# doorDash-delivery-data-processing
# Project Summary: Processing for DoorDash Delivery Data

## Overview
This project aims to automate the processing of daily delivery data from DoorDash using AWS services. JSON files containing delivery records will be uploaded to an Amazon S3 bucket (`doordash-landing-sa`). An AWS Lambda function, triggered by file uploads, will filter the records based on the delivery status and save the filtered data to another S3 bucket (`doordash-target-sa`). Notifications regarding the processing outcome will be sent via Amazon SNS.

## Requirements
- AWS Account
- Amazon S3 buckets: `doordash-landing-sa` and `doordash-target-sa`
- AWS Lambda
- Amazon SNS
- AWS IAM (for permissions)
- AWS CodeBuild (for CI/CD)
- GitHub (for version control)
- Python, pandas library
- Email subscription for SNS notifications

## Steps
1. **Sample JSON File for Daily Data:** A sample JSON file named `yyyy-mm-dd-raw_input.json` with 10 delivery records, including different statuses like cancelled, delivered, and order placed.

2. **Set Up S3 Buckets:** Create two S3 buckets: `doordash-landing-sa` for incoming raw files and `doordash-target-sa` for processed files.

3. **Set Up Amazon SNS Topic:** Create an SNS for sending processing notifications. Subscribe to an email to the topic to receive notifications.

4. **Create IAM Role for Lambda:** Create an IAM role with permissions to read from `doordash-landing-sa`, write to `doordash-target-sa`, and publish messages to the SNS topic.

5. **Create and Configure AWS Lambda Function:**
   - Create a Lambda function using Python runtime.
   - Include the pandas library in the function's deployment package or use a Lambda Layer for pandas.
   - Use the S3 trigger to invoke the function upon file uploads to `doordash-landing-sa`.
   - The Lambda function should:
     - Read the JSON file into a pandas DataFrame.
     - Filter records where status is "delivered".
     - Write the filtered DataFrame to a new JSON file in `doordash-target-sa`.
     - Publish a success or failure message to the SNS topic.

6. **AWS CodeBuild for CI/CD:** Host your Lambda function code on GitHub. Set up an AWS CodeBuild project linked to your GitHub repository. Configure the `buildspec.yml` to automate your Lambda function code update deployment.

7. **Testing and Verification:** Upload the sample JSON file to `doordash-landing-sa` and verify that the Lambda function triggers correctly. Check `doordash-target-sa` for the processed file and confirm its contents. Ensure an email notification is received upon processing completion.

This project streamlines the processing of DoorDash delivery data using AWS services, enhancing operational workflows and ensuring efficiency and reliability.
