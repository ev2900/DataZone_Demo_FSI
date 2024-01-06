# DataZone Demo with Financial Services Specific Data

This repository provides an easy way to deply and set up an environment for demo'ing Amazon DataZone with data sets specific to the financial services industry.

The demo data sets used are in the [Data_Sets](https://github.com/ev2900/DataZone_Demo_FSI/tree/main/Data_Sets) folder. Each data set has a CSV file with 100 sample rows of data and a README describing the dataset. All of the data in each data set is fictonal data created for the purposes of demonstrating DataZone.

## Instructions to deploy the demo an in AWS account

1. Launch the CloudFormation stack

[![Launch CloudFormation Stack](https://sharkech-public.s3.amazonaws.com/misc-public/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=data-zone-fsi&templateURL=https://sharkech-public.s3.amazonaws.com/misc-public/0_data_zone_fsi_cloudformation.yaml)

2. Run the following from the terminal of the [Cloud9](https://us-east-1.console.aws.amazon.com/cloud9control/home) environment that was deployed by the CloudFormation stack

```pip install -r DataZone_Demo_FSI/requirements.txt```

```python DataZone_Demo_FSI/1_copy_data_sets_to_s3.py```

```python DataZone_Demo_FSI/2_set_up_glue_data_catalog.py```

```python DataZone_Demo_FSI/3_set_up_redshift.py```

