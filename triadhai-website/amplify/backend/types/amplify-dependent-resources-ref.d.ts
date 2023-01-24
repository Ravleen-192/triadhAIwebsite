export type AmplifyDependentResourcesAttributes = {
    "function": {
        "sendWPMail": {
            "Name": "string",
            "Arn": "string",
            "Region": "string",
            "LambdaExecutionRole": "string"
        },
        "AddtoDB": {
            "Name": "string",
            "Arn": "string",
            "Region": "string",
            "LambdaExecutionRole": "string"
        }
    },
    "api": {
        "SendWPMail": {
            "RootUrl": "string",
            "ApiName": "string",
            "ApiId": "string"
        }
    }
}