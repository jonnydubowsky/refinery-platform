/*! refinery-platform-ui 2015-06-16 */

var hideChildNodes=function(a){a.children.empty()||a.children.values().forEach(function(a){a.hidden=!0,d3.selectAll("#nodeId-"+a.autoId).classed({selectedNode:!1,hiddenNode:!0}),a.children.empty()||hideChildNodes(a)})},propagateNodeSelection=function(a,b){a.children.empty()||a.children.values().forEach(function(a){a.selected=b,a.doi.selectedChanged(),a.children.empty()||propagateNodeSelection(a,b)})},customTimeFormat=function(a){return d3.time.format("%Y-%m-%d %H:%M:%S %p")(a)},parseISOTimeFormat=function(a){var b=d3.time.format("%Y-%m-%dT%H:%M:%S.%L");return b.parse(a)},compareMaps=function(a,b){var c=!0;return a.size()===b.size()?a.keys().forEach(function(a){b.has(a)||(c=!1)}):c=!1,c},getLayerPredCount=function(a){return a.children.values().map(function(a){return a.predLinks.size()}).reduce(function(a,b){return a+b})},getLayerSuccCount=function(a){return a.children.values().map(function(a){return a.succLinks.size()}).reduce(function(a,b){return a+b})},bfs=function(a){var b=function(a){a.succs.values().forEach(function(a){a instanceof provvisDecl.Node&&-1===d.indexOf(a.parent.parent)?(d.push(a.parent.parent),c.push(a.parent.parent)):-1===d.indexOf(a)&&(d.push(a),c.push(a))})},c=[],d=[];for(d.push(a),c.push(a);c.length>0;)b(c.shift())};
//# sourceMappingURL=provvis_helpers.js.map