puppet-enc-ec2
==============

A Puppet ENC which assigns Nodes based on their AWS EC2 Tags. Additionally, all
EC2 Tags are made available to Puppet as trusted Top Level Variables with the
``ec2_tag_`` prefix.


Problem summary
---------------

Historically, I used the `ec2tagfacts`_ module to classify Puppet Nodes in AWS
EC2. This works great! The Puppet Agents enumerate their own EC2 Tags using the
module and they report the Tags to the Puppet Master as Untrusted Facts. These
Facts can then be used by the Enterprise Node Classifier to assign Classes to
the Node.

By example, I created an ``Environment`` and ``Role`` tag in EC2 that are
reported by the Puppet Agent and used to assign the Node to the matching
Puppet Environment and Role class.

There are a few problems with this approach:

* Every EC2 Instance must be assigned permission to read its own tags, and
  consequently, the tags of any other EC2 Instance
* A managed agent could spoof the EC2 Tag Facts to retrieve configuration for
  and other class or environment
* When using the Puppet Enterprise console, a Classification Group had to be
  created for every Role in every Environment

This solution mitigates these issues as:

* Only the Puppet Master needs permission to read tags
* EC2 tags are provided by the ENC as Top Level Variables - these cannot be
  spoofed by an agent and are therefore more secure
* No additional configuration is required in the Enterprise Console

.. _ec2tagfacts: https://www.bryanandrews.org/ec2tagfacts/


Usage
-----

This ENC assumes you are using the `Roles and Profiles`_ paradigm and intend to
assign a single Role class to each node, with the ``role::`` prefix.

Each managed EC2 Instance must have the following EC2 Tags assigned:

* ``Environment`` - The Puppet Environment to assign (default: ``production``)
* ``Role`` - the Role class to assign, excluding the ``role::`` prefix

.. _Roles and Profiles: https://puppet.com/docs/pe/latest/managing_nodes/roles_and_profiles_example.html


Installation
------------

Install the classifier on your Puppet Master with the following:

.. code-block:: shell

    $ pip install puppet-enc-ec2

    # or

    $ curl -o /usr/local/bin/puppet-enc-ec2 \
        https://raw.githubusercontent.com/cavaliercoder/puppet-enc-ec2/master/bin/puppet-enc-ec2
    $ chmod +x /usr/local/bin/puppet-enc-ec2


Configure the Puppet Master to use the executable Node Classifier in
``puppet.conf`` as follows:

.. code-block:: ini

    [master]
      node_terminus = exec
      external_nodes = /usr/local/bin/puppet-enc-ec2


The Puppet Master will also need the following IAM Policy applied so that is can
query the EC2 API for Instance metadata:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["ec2:DescribeInstances"],
                "Resource": "*"
            }
        ]
    }

For for information about installing a custom ENC, see:
https://puppet.com/docs/puppet/latest/nodes_external.html


Configuration
-------------

The script uses the Amazon AWS SDK (``boto3``) to connect to AWS. The SDK must
be configured with credentials to connect to the AWS APIs. Please see the `Boto3
documentation`_ for instruction.

.. _Boto3 Documentation: http://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration

In addition, the desired AWS Region should be configured by modifying the
script, or setting the ``AWS_DEFAULT_REGION`` environment variable.


Example
-------

.. code-block:: shell

    # test the classifier for an EC2 Instance
    $ puppet-enc-ec2 i-deadbeefcafebabe
    ---
    classes:
      role::web_server:
    environment: production
    parameters:
      ec2_tag_name: WebServer
      ec2_tag_description: Web Application Server
      ec2_tag_environment: production
      ec2_tag_role: web_server
      ec2_tag_aws_cloudformation_logical_id: WebServer
      ec2_tag_aws_cloudformation_stack_id: arn:aws:cloudformation:us-east-1:123456789000:stack/cf-web-server/0f7b6bb0-9d1a-11e7-848e-50fa575f68fe
      ec2_tag_aws_cloudformation_stack_name: cf-web-server
      ec2_tags:
        Name: WebServer
        Description: Web Application Server
        Environment: production
        Role: web_server
        aws:cloudformation:logical-id: WebServer
        aws:cloudformation:stack-id: arn:aws:cloudformation:us-east-1:123456789000:stack/cf-web-server/0f7b6bb0-9d1a-11e7-848e-50fa575f68fe
        aws:cloudformation:stack-name: cf-web-server
