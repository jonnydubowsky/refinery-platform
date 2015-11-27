describe('RefineryApp.module: unit tests', function () {
  'use strict';

  var module;

  beforeEach(function () {
    module = angular.module('refineryApp');
  });

  describe('Module', function () {

    it('should be registered', function () {
      expect(!!module).toEqual(true);
    });

  });

  describe('Dependencies:', function () {

    var deps,
        hasModule = function (m) {
          return deps.indexOf(m) >= 0;
        };

    beforeEach(function () {
      deps = module.value('refineryApp').requires;
    });

    it('should have "ngResource" as a dependency', function () {
      expect(hasModule('ngResource')).toEqual(true);
    });

    it('should have "ui.router" as a dependency', function () {
      expect(hasModule('ui.router')).toEqual(true);
    });

    it('should have "ngWebworker" as a dependency', function () {
      expect(hasModule('ngWebworker')).toEqual(true);
    });

    it('should have "pubSub" as a dependency', function () {
      expect(hasModule('pubSub')).toEqual(true);
    });

    it('should have "closeOnOuterClick" as a dependency', function () {
      expect(hasModule('closeOnOuterClick')).toEqual(true);
    });

    it('should have "colors" as a dependency', function () {
      expect(hasModule('colors')).toEqual(true);
    });

    it('should have "refineryRouter" as a dependency', function () {
      expect(hasModule('refineryRouter')).toEqual(true);
    });

    it('should have "refineryWorkflows" as a dependency', function () {
      expect(hasModule('refineryWorkflows')).toEqual(true);
    });

    it('should have "refineryNodeMapping" as a dependency', function () {
      expect(hasModule('refineryNodeMapping')).toEqual(true);
    });

    it('should have "refineryAnalysisLaunch" as a dependency', function () {
      expect(hasModule('refineryAnalysisLaunch')).toEqual(true);
    });

    it('should have "refinerySolr" as a dependency', function () {
      expect(hasModule('refinerySolr')).toEqual(true);
    });

    it('should have "refineryNodeRelationship" as a dependency', function () {
      expect(hasModule('refineryNodeRelationship')).toEqual(true);
    });

    it('should have "refineryIgv" as a dependency', function () {
      expect(hasModule('refineryIgv')).toEqual(true);
    });

    it('should have "refineryStatistics" as a dependency', function () {
      expect(hasModule('refineryStatistics')).toEqual(true);
    });

    it('should have "refineryMetadataTableImport" as a dependency', function () {
      expect(hasModule('refineryMetadataTableImport')).toEqual(true);
    });

    it('should have "refineryProvvis" as a dependency', function () {
      expect(hasModule('refineryProvvis')).toEqual(true);
    });

    it('should have "refineryDataSetImport" as a dependency', function () {
      expect(hasModule('refineryDataSetImport')).toEqual(true);
    });

    it('should have "refineryDataSetNav" as a dependency', function () {
      expect(hasModule('refineryDataSetNav')).toEqual(true);
    });

    it('should have "refineryDashboard" as a dependency', function () {
      expect(hasModule('refineryDashboard')).toEqual(true);
    });

    it('should have "refineryAnalysisMonitor" as a dependency', function () {
      expect(hasModule('refineryAnalysisMonitor')).toEqual(true);
    });

    it('should have "refineryCollaboration" as a dependency', function () {
      expect(hasModule('refineryCollaboration')).toEqual(true);
    });

    it('should have "refineryChart" as a dependency', function () {
      expect(hasModule('refineryChart')).toEqual(true);
    });

    // Just a negative control to make sure that the test actually works.
    it('should NOT have "notExistingModule" as a dependency', function () {
      expect(hasModule('notExistingModule')).toEqual(false);
    });

  });
});