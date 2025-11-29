"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.WAHATriggerV202502 = void 0;
const doc = __importStar(require("./openapi.json"));
const trigger_1 = require("../base/trigger");
function getEvents() {
    const schemas = doc.components.schemas;
    const schema = schemas.WAHAWebhookSessionStatus;
    const event = schema.properties.event;
    return event.enum;
}
const events = getEvents();
const outputs = events.map((_) => "main");
const outputNames = events;
class WAHATriggerV202502 {
    constructor() {
        this.description = {
            ...trigger_1.BASE_TRIGGER_DESCRIPTION,
            ...trigger_1.TRIGGER_DESCRIPTION,
            version: 202502,
            outputs: outputs,
            outputNames: outputNames,
            properties: [trigger_1.CONFIGURE_WEBHOOK_NOTE, (0, trigger_1.makeEventNote)(events)],
        };
        this.webhook = (0, trigger_1.makeWebhookForEvents)(events);
    }
}
exports.WAHATriggerV202502 = WAHATriggerV202502;
//# sourceMappingURL=WAHATriggerV202502.js.map