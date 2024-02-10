# DataZone Demo with Financial Services Specific Data

<img width="275" alt="map-user" src="https://img.shields.io/badge/cloudformation template deployments-31-blue"> <img width="85" alt="map-user" src="https://img.shields.io/badge/views-1493-green"> <img width="125" alt="map-user" src="https://img.shields.io/badge/unique visits-034-green">

This repository provides an easy way to deploy and set up an environment for demo'ing Amazon DataZone with data sets specific to the financial services industry.

The demo data sets used are in the [Data_Sets](https://github.com/ev2900/DataZone_Demo_FSI/tree/main/Data_Sets) folder. Each data set has a CSV file with 100 sample rows of data and a README describing the dataset. All of the data in each data set is fictional data created for the purposes of demonstrating DataZone.

## Instructions to deploy the demo an in AWS account

1. Launch the CloudFormation stack

[![Launch CloudFormation Stack](https://sharkech-public.s3.amazonaws.com/misc-public/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=data-zone-fsi&templateURL=https://sharkech-public.s3.amazonaws.com/misc-public/0_data_zone_fsi_cloudformation.yaml)

2. Run the following from the terminal of the [Cloud9](https://us-east-1.console.aws.amazon.com/cloud9control/home) environment that was deployed by the CloudFormation stack

```pip install -r DataZone_Demo_FSI/requirements.txt```

```python DataZone_Demo_FSI/1_copy_data_sets_to_s3.py```

```python DataZone_Demo_FSI/2_set_up_glue_data_catalog.py```

```python DataZone_Demo_FSI/3_set_up_redshift.py```

3. Deploy a DataZone domain from the AWS console

* Navigate to the [DataZone](https://us-east-1.console.aws.amazon.com/datazone/home) home page and click on **Create domain**
* Provide a name for the domain
* Select the check mark next to the *Set-up this account for data consumption and publishing* under the Quick setup section

<img width="500" alt="quick_setup" src="https://github.com/ev2900/DataZone_Demo_FSI/blob/main/README/quick_setup_button.png">

* Click on **Create domain**

4. Update the ```datazone_domain_id``` variable in [4_set_up_datazone.py](https://github.com/ev2900/DataZone_Demo_FSI/blob/main/4_set_up_datazone.py)

To find the domain id of the DataZone domain you just deployed look at the URL for the DataZone portal

For example if the URL is https//dzd_498d049z6o1gkn.datazone.us-east-1.on.aws the domain id is dzd_498d049z6o1gkn

Once you update the variables with the domain id **save the file**

5. Run the following from the terminal of the [Cloud9](https://us-east-1.console.aws.amazon.com/cloud9control/home) environment

```python DataZone_Demo_FSI/4_set_up_datazone.py```

**Note** *run the 4_set_up_datazone.py script twice. Not all resources will successfully deploy on the first run*
