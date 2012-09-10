from celery.result import AsyncResult, TaskSetResult
from core.models import Analysis
from django.db import models
from django_extensions.db.fields import UUIDField
import math


'''
shift+command+o // cleans up imports 

http://permalink.gmane.org/gmane.comp.python.amqp.celery.user/2036

from celery.task import TaskSet
   from celery.result import TaskSetResult

   ts_result = TaskSet(add.subtask((i, i)) for i in
xrange(10)).apply_async()
   ts_result.save()
   taskset_id = ts_result.taskset_id

   # later
   ts_result = TaskSetResult.restore(taskset_id)
'''

class AnalysisStatus( models.Model ):
    analysis = models.ForeignKey(Analysis)
    #analysis_uuid = UUIDField( unique=True, auto=False )
    
    preprocessing_taskset_id = UUIDField( blank=True, null=True, auto=False )
    execution_taskset_id = UUIDField( blank=True, null=True, auto=False )
    postprocessing_taskset_id = UUIDField( blank=True, null=True, auto=False )
    cleanup_taskset_id = UUIDField( blank=True, null=True, auto=False )
    execution_monitor_task_id = UUIDField( blank=True, null=True, auto=False )
    
    def preprocessing_status(self):
        return getPayload(self.preprocessing_taskset_id)
    
    def execution_status(self):
        total_steps = Analysis.objects.get(uuid=self.analysis.uuid).workflow_steps_num        
        test = getPayload(self.execution_monitor_task_id)
        #print "test lgneth"
        #print len(test)
            
        test[0]['total_steps'] = total_steps
        if 'ok' in test[0].keys():
            test[0]['percent_done'] =  str(100*float(test[0]['ok'])/float(total_steps)) + '%'
        else:
            test[0]['percent_done'] = '0%'
        return test
    
    def postprocessing_status(self):
        return getPayload(self.postprocessing_taskset_id)
    
    def cleanup_status(self):
        return getPayload(self.cleanup_taskset_id)
  

def getPayload(ts_id):
    #print "getPayload \n"
    
    payload = []
    ts = AsyncResult( ts_id )
    if ts:
        if ts.result:
            if type(ts.result) ==type(dict()):
                if type(ts.result['message']) ==type(dict()):
                    temp_ret = ts.result['message']
                else:
                    temp_ret = ts.result
                temp_ret['state'] = ts.state
                temp_ret['task_id'] = ts.task_id
                payload.append(temp_ret)
            elif (ts.result.__class__.__name__ == 'TaskSetResult'):
                n_tasks = len(ts.result.results)
                if n_tasks > 0:
                    for j in range(0,n_tasks):
                        temp_ret = {};
                        if ts.result.results[j].result:
                            if ts.result.results[j].result.__class__.__name__ == 'FileStoreItem':
                                temp_ret['state'] = ts.result.results[j].state
                                temp_ret['task_id'] = ts.result.results[j].task_id
                                payload.append(temp_ret)
                            else:
                                # if result returns as dictionary
                                if type(ts.result.results[j].result) ==type(dict()):
                                    temp_ret = ts.result.results[j].result
                                    
                                # if result is just a string
                                else: 
                                    #print "-------------"
                                    #print "PAYLOAD TEST"
                                    #print "j"
                                    #print j
                                    #print "results all"
                                    #print ts.result.results[j]
                                    #print "result"
                                    #print ts.result.results[j].result
                                    #print "state"
                                    #print ts.result.results[j].state
                                    
                                    temp_ret = {}
                                    
                                temp_ret['state'] = str(ts.result.results[j].state)
                                temp_ret['task_id'] = str(ts.result.results[j].task_id)
                                payload.append(temp_ret)
                                
                        else:
                            temp_ret['state'] = ts.result.results[j].state
                            temp_ret['task_id'] = ts.result.results[j].task_id
                            payload.append(temp_ret)
                #else:
                #    print "00000 tasks"
                #    print ts.result
            else:
                temp_ret = {'state':ts.state, 'info':str(ts.result), 'task_id':ts.task_id}
                payload.append(temp_ret)
        else:
            temp_ret = {'state':ts.state, 'task_id':ts.task_id}
            payload.append(temp_ret)
    else:
        temp_ret = {'state':"### WAITING ###"}
        payload.append(temp_ret)
    
    #print "payload called"
    #print "################################"
    #print payload 
    #print len(payload)
    #print "################################"
            
    return payload

