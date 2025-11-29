import { INodeProperties, INodeTypeBaseDescription, WebhookType, type IWebhookFunctions, type IWebhookResponseData } from 'n8n-workflow';
export declare const BASE_TRIGGER_DESCRIPTION: INodeTypeBaseDescription;
export declare const TRIGGER_DESCRIPTION: {
    defaults: {
        name: string;
    };
    inputs: never[];
    credentials: never[];
    webhooks: {
        name: WebhookType;
        httpMethod: string;
        responseMode: string;
        path: string;
    }[];
};
export declare const CONFIGURE_WEBHOOK_NOTE: INodeProperties;
export declare function makeEventNote(events: string[]): INodeProperties;
export declare function makeWebhookForEvents(events: string[]): (this: IWebhookFunctions) => Promise<IWebhookResponseData>;
