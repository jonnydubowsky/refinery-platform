/*! refinery-platform-ui 2015-06-16 */

angular.module("refineryApp",["refineryWorkflows","refineryNodeMapping","refineryAnalysis","refinerySolr","refineryExternalToolStatus","refineryNodeRelationship","refineryIgv","refineryStatistics","refineryMetadataTableImport","refineryProvvis","refinerySharing","refineryDataFileUpload"]).config(["$provide",function(a){a.decorator("$rootScope",["$delegate",function(a){return Object.defineProperty(a.constructor.prototype,"$onRootScope",{value:function(b,c){var d=a.$on(b,c);this.$on("$destroy",d)},enumerable:!1}),a}])}]).constant("$",jQuery);
//# sourceMappingURL=refinery.js.map