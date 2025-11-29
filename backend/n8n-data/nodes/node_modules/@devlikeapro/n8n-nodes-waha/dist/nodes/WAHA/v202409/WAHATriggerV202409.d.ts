import { INodeType, INodeTypeDescription } from 'n8n-workflow';
export declare class WAHATriggerV202409 implements INodeType {
    description: INodeTypeDescription;
    webhook: (this: import("n8n-workflow").IWebhookFunctions) => Promise<import("n8n-workflow").IWebhookResponseData>;
}
