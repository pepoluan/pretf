## Starting code

Let's start by showing `animals.tf.py` from the previous pages, plus a new file `users.tf.py`. We can see that these files are hardcoding their data: the lists of animals and users.

```python
# animals.tf.py

from pretf.api import tf


def terraform(var):
    animals = ["dog", "cat", "buffalo", "rabbit", "badger"]  # hardcoded
    for name in animals:
        animal = yield tf(f"resource.random_integer.{name}", {
            "min": 1,
            "max": 10,
        })
        yield tf(f"output.{name}", {
            "vaue": animal.result,
        })
```

```python
# users.tf.py

from pretf.api import tf


def terraform(var):
    users = ["ray", "violet"]  # hardcoded
    for name in users:
        yield tf(f"resource.aws_iam_user.{name}", {"name": name})
```

## Terraform variables

Teraform variables can be access using the `var` argument passed into `terraform()` functions. Let's use them instead of hardcoding the values:


```terraform
# variables.tf

variable "animals" {
  type = list(string)
}

variable "users" {
  type = list(string)
}
```

```terraform
# terraform.tfvars

animals = ["dog", "cat", "buffalo", "rabbit", "badger"]

users = ["ray", "violet"]
```

```python
# animals.tf.py

from pretf.api import tf


def terraform(var):
    for name in var.animals: # using terraform variables
        animal = yield tf(f"resource.random_integer.{name}", {
            "min": 1,
            "max": 10,
        })
        yield tf(f"output.{name}", {
            "vaue": animal.result,
        })
```

```python
# users.tf.py

from pretf.api import tf


def terraform(var):
    for name in var.users: # using terraform variables
        yield tf(f"resource.aws_iam_user.{name}", {"name": name})
```

# Variable definition precedence

From the [Terraform documentation](https://www.terraform.io/docs/configuration/variables.html#variable-definition-precedence
):

<blockquote>
    <p>Terraform loads variables in the following order, with later sources taking precedence over earlier ones:</p>
    <ul>
        <li>Environment variables.</li>
        <li>The <code>terraform.tfvars</code> file, if present.</li>
        <li>The <code>terraform.tfvars.json</code> file, if present.</li>
        <li>Any <code>*.auto.tfvars</code> or <code>*.auto.tfvars.json</code> files, processed in lexical order of their filenames.</li>
        <li> Any <code>-var</code> and <code>-var-file</code> options on the command line, in the order they are provided.</li>
    </ul>
</blockquote>

Pretf uses the same rules when resolving variable values, with one exception. If a project has `*.tfvars.py` files to generate `*.tfvars.json` files then those files will have the lowest precedence, i.e. all other sources will be checked first.

As a result, it is possible for Pretf and Terraform to have different variable values in cases where values are being set in multiple places. Because of this, it is recommended to set variable values in only one place.