import { OpenAPIV3 } from 'openapi-types';
import { DefaultOperationParser, OperationContext } from '@devlikeapro/n8n-openapi-node';
export declare class WAHAOperationParser extends DefaultOperationParser {
    name(operation: OpenAPIV3.OperationObject, context: OperationContext): string;
    value(operation: OpenAPIV3.OperationObject, context: OperationContext): string;
    action(operation: OpenAPIV3.OperationObject, context: OperationContext): string;
    description(operation: OpenAPIV3.OperationObject, context: OperationContext): string;
}
