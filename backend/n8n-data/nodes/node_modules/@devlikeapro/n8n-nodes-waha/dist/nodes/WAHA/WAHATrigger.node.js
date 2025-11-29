"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WAHATrigger = void 0;
const n8n_workflow_1 = require("n8n-workflow");
const trigger_1 = require("./base/trigger");
const WAHATriggerV202409_1 = require("./v202409/WAHATriggerV202409");
const WAHATriggerV202502_1 = require("./v202502/WAHATriggerV202502");
class WAHATrigger extends n8n_workflow_1.VersionedNodeType {
    constructor() {
        const baseDescription = {
            ...trigger_1.BASE_TRIGGER_DESCRIPTION,
            defaultVersion: 202502,
        };
        const nodeVersions = {
            202502: new WAHATriggerV202502_1.WAHATriggerV202502(),
            202409: new WAHATriggerV202409_1.WAHATriggerV202409(),
        };
        super(nodeVersions, baseDescription);
    }
}
exports.WAHATrigger = WAHATrigger;
//# sourceMappingURL=WAHATrigger.node.js.map