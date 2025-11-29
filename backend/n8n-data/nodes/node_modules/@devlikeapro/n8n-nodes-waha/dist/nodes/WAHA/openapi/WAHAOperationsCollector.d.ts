import { OpenAPIV3 } from 'openapi-types';
import { INodeProperties } from 'n8n-workflow';
import { OperationsCollector, OperationContext } from '@devlikeapro/n8n-openapi-node';
export declare class WAHAOperationsCollector extends OperationsCollector {
    parseFields(operation: OpenAPIV3.OperationObject, context: OperationContext): INodeProperties[];
}
