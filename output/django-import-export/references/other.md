# Django-Import-Export - Other

**Pages:** 17

---

## Frequently Asked Questions — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/faq.html

**Contents:**
- Frequently Asked Questions
- What’s the best way to communicate a problem, question, or suggestion?
- How can I help?
- Common issues
  - import_id_fields error on import
  - How to handle double-save from Signals
  - How to dynamically set resource values
  - How to set a value on all imported instances prior to persisting
  - How to export from more than one table
  - How to import imagefield in excel cell

To submit a feature, to report a bug, or to ask a question, please refer our contributing guidelines.

We welcome contributions from the community.

You can help in the following ways:

Reporting bugs or issues.

Answering questions which arise on Stack Overflow or as Github issues.

Providing translations for UI text.

Suggesting features or changes.

We encourage you to read the contributing guidelines.

The following error message can be seen on import:

The following fields are declared in ‘import_id_fields’ but are not present in the resource

This indicates that the Resource has not been configured correctly, and the import logic fails. Specifically, the import process is attempting to use either the defined or default values for import_id_fields and no matching field has been detected in the resource fields. See Create or update model instances.

In cases where you are deliberately using generated fields in import_id_fields and these fields are not present in the dataset, then you need to modify the resource definition to accommodate this. See Using ‘dynamic fields’ to identify existing instances.

This issue can apply if you have implemented post-save Signals, and you are using the import workflow in the Admin interface. You will find that the post-save signal is called twice for each instance. The reason for this is that the model save() method is called twice: once for the ‘confirm’ step and once for the ‘import’ step. The call to save() during the ‘confirm’ step is necessary to prove that the object will be saved successfully, or to report any exceptions in the Admin UI if save failed. After the ‘confirm’ step, the database transaction is rolled back so that no changes are persisted.

Therefore there is no way at present to stop save() being called twice, and there will always be two signal calls. There is a workaround, which is to set a temporary flag on the instance being saved:

Your signal receiver can then include conditional logic to handle this flag:

Further discussion here and here.

There can be use cases where you need a runtime or user supplied value to be passed to a Resource. See How to dynamically set resource values.

If you need to set the same value on each instance created during import then refer to How to set a value on all imported instances prior to persisting.

In the usual configuration, a Resource maps to a single model. If you want to export data associated with relations to that model, then these values can be defined in the fields declaration. See Model relations.

Please refer to this issue.

Please refer to How to format UI error messages.

When importing using the Admin site, it can be that the ids of the imported instances are different from those show in the preview step. This occurs because the rows are imported during ‘confirm’, and then the transaction is rolled back prior to the confirm step. Database implementations mean that sequence numbers may not be reused.

Consider enabling IMPORT_EXPORT_SKIP_ADMIN_CONFIRM as a workaround.

See this issue for more detailed discussion.

This was an issue in v3 which is resolved in v4. The issue arises when importing from Excel because empty cells are converted to None during import. If the import process attempted to save a null value then a ‘NOT NULL’ exception was raised.

In v4, initialization checks to see if the Django CharField has blank set to True. If it does, then null values or empty strings are persisted as empty strings.

If it is necessary to persist None instead of an empty string, then the allow_blank widget parameter can be set:

It is possible to reference model relations by defining a field with the double underscore syntax. For example:

This means that during export, the relation will be followed and the referenced field will be added correctly to the export.

It works the same way when using attribute in Field. For example:

This does not work during import because the reference may not be enough to identify the correct relation instance. ForeignKeyWidget should be used during import. See the documentation explaining Foreign Key relations.

See the following responses on StackOverflow:

https://stackoverflow.com/a/55046474/39296

https://stackoverflow.com/questions/74802453/export-only-the-data-registered-by-the-user-django-import-export

If you want more control over how export data is formatted when exporting to Excel you can write a custom format which uses the openpyxl API. See the example here.

If export produces garbled or unexpected output, you may need to set the export encoding. See this issue.

See Creating non-existent relations.

If uploading large files, you may encounter time-outs. See Using celery and Bulk imports.

This could be due to hidden rows in Excel files. Hidden rows can be excluded using IMPORT_EXPORT_IMPORT_IGNORE_BLANK_LINES.

Refer to this PR for more information.

See Foreign Key relations.

This can occur if a model defines a __str__() method which references a primary key or foreign key relation, and which is None during import. There is a workaround to deal with this issue. Refer to this comment.

This indicates that the change_list_template attribute could not be set, most likely due to a clash with a third party library. Refer to Interoperability with 3rd party libraries.

Refer to this comment.

You may receive an error during import such as:

This usually happens because you are running the Admin site in a multi server or container environment. During import, the import file has to be stored temporarily and then retrieved for storage after confirmation. Therefore FileNotFoundError error can occur because the temp storage is not available to the server process after confirmation.

To resolve this, you should avoid using temporary file system storage in multi server environments.

Refer to Import confirmation for more information.

Large datasets can be exported in a number of ways, depending on data size and preferences.

You can write custom scripts or Admin commands to handle the export. Output can be written to a local filesystem, cloud bucket, network storage etc. Refer to the documentation on exporting programmatically.

You can use the third party library django-import-export-celery to handle long-running exports.

You can enable export via admin action and then select items for export page by page in the Admin UI. This will work if you have a relatively small number of pages and can handle export to multiple files. This method is suitable as a one-off or as a simple way to export large datasets via the Admin UI.

If you want to modify the names of the columns on export, you can do so by overriding get_export_headers():

Refer to logging configuration for more information.

This occurs when your data contains a character which cannot be rendered in Excel. You can configure import-export to sanitize these characters.

---

## Bulk imports — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/bulk_import.html

**Contents:**
- Bulk imports
- Caveats
- ForeignKeyWidget performance considerations
- Performance tuning
- Testing

import-export provides a ‘bulk mode’ to improve the performance of importing large datasets.

In normal operation, import-export will call instance.save() as each row in a dataset is processed. Bulk mode means that instance.save() is not called, and instances are instead added to temporary lists. Once the number of rows processed matches the batch_size value, then either bulk_create() or bulk_update() is called.

If batch_size is set to None, then bulk_create() / bulk_update() is only called once all rows have been processed.

Bulk deletes are also supported, by applying a filter() to the temporary object list, and calling delete() on the resulting query set.

The model’s save() method will not be called, and pre_save and post_save signals will not be sent.

bulk_update() is only supported in Django 2.2 upwards.

Bulk operations do not work with many-to-many relationships.

Take care to ensure that instances are validated before bulk operations are called. This means ensuring that resource fields are declared appropriately with the correct widgets. If an exception is raised by a bulk operation, then that batch will fail. It’s also possible that transactions can be left in a corrupted state. Other batches may be successfully persisted, meaning that you may have a partially successful import.

In bulk mode, exceptions are not linked to a row. Any exceptions raised by bulk operations are logged and returned as critical (non-validation) errors (and re-raised if raise_errors is true).

If there is the potential for concurrent writes to a table during a bulk operation, then you need to consider the potential impact of this. Refer to Concurrent writes for more information.

For more information, please read the Django documentation on bulk_create() and bulk_update().

When using ForeignKeyWidget, the related object is looked up using QuerySet.get() during import. This lookup occurs once per imported row. For large imports, this can result in a significant number of database queries and impact performance.

You can subclass ForeignKeyWidget and override get_queryset() to limit the pool of candidate objects. However, overriding get_queryset() alone does not necessarily eliminate per-row database queries, because ForeignKeyWidget.clean() calls .get() for each row.

If import performance is critical, consider using CachedForeignKeyWidget instead. This widget caches all related objects in memory before the import begins, eliminating per-row database queries.

Consider the following if you need to improve the performance of imports.

Enable use_bulk for bulk create, update and delete operations (read Caveats first).

If your import is creating instances only (i.e. you are sure there are no updates), then set force_init_instance = True.

If your import is updating or creating instances, and you have a set of existing instances which can be stored in memory, use CachedInstanceLoader

If your import has relations on per-row basis, consider using CachedForeignKeyWidget for ForeignKey fields.

By default, import rows are compared with the persisted representation, and the difference is stored against each row result. If you don’t need this diff, then disable it with skip_diff = True.

Setting batch_size to a different value is possible, but tests showed that setting this to None always resulted in worse performance in both duration and peak memory.

Scripts are provided to enable testing and benchmarking of bulk imports. See Bulk testing.

---

## Export workflow — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/export_workflow.html

**Contents:**
- Export workflow

This document describes the export data workflow in detail, with hooks that enable customization of the export process.

Methods highlighted in yellow in the sequence diagram indicate public methods which can be overridden.

The export() method retrieves a QuerySet from the database and formats into a tablib.Dataset.

Various hook methods are defined to allow you to customize the export data.

This is what happens when the method is invoked:

The export() method is passed an optional queryset parameter. The kwargs dict can hold additional information used to create the export, for example if called from the Admin UI.

The before_export() hook is called.

If no QuerySet has been passed, then get_queryset() method is called.

The filter_export() hook is called. You can override this method to modify the queryset for export.

For each instance in the QuerySet, export_resource() is called (with the instance passed as a parameter).

For each field defined in fields:

export_field() is called with the field and instance as parameters.

If a dehydrate method is defined on the Resource, then this method is called to extract the field value, Otherwise export() is called for each defined field, with the instance passed as a parameter.

get_value() is called with the instance to retrieve the export value from the instance.export

The field’s widget render() method is called to retrieve the export value.

Each value is appended to a tablib.Dataset.

The tablib.Dataset is returned from export().

---

## Django import / export — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/

**Contents:**
- Django import / export

django-import-export is a Django application and library for importing and exporting data with included admin integration.

Import from / Export to multiple file formats

Manage import / export of object relations, data types

Handle create / update / delete / skip during imports

Support multiple formats (Excel, CSV, JSON, … and everything else that tablib supports)

Admin integration for importing / exporting

Preview import changes

Export data respecting admin filters

A screenshot of the change view with Import and Export buttons.

---

## Release Notes — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/release_notes.html

**Contents:**
- Release Notes
- v5.0
  - Breaking changes
  - Deprecations
- v4.2
  - Breaking changes
- v4.1
- v4.0
  - Installation
  - Functional changes

This release fixes an issue with form field name clashes (see 2108).

If you have any customizations which rely on form field names then you may need to make some adjustments as a result of this change.

The resource, format and export_items field names are now prepended with django-import-export-.

Removed the deprecated get_valid_export_item_pks() method in favour of get_queryset(). Use the ModelAdmin’s get_queryset() or get_export_queryset() instead.

Fixed issue where export forms were incorrectly showing import fields instead of export fields. This was resolved by introducing context-specific methods for field retrieval. See deprecations and PR 2118.

The get_user_visible_fields() method is now deprecated and will be removed in version 6.0. Use get_user_visible_import_fields() for import contexts and get_user_visible_export_fields() for export contexts instead. This change ensures that import and export operations show their respective field sets correctly in admin forms.

When exporting via admin action, the queryset is now filtered on get_queryset() instead of the Model’s default queryset. This should have no impact on existing implementations.

This change also made get_valid_export_item_pks() obsolete, as the ModelAdmin’s get_export_queryset(), or ModelAdmin’s get_queryset can be used instead. The get_valid_export_item_pks() method is now deprecated.

Removed internal method _get_enabled_export_fields() in favour of passing the selected fields list as a new parameter to export_resource() and get_export_headers().

Hide the “Resource” form when it only has one option, to avoid potentially confusing text in the interface like “Resource: BookResource”. To undo this change, use a form subclass that changes the field’s widget to a django.forms.Select. See 1908

tablib has been upgraded from v3.5.0 to 3.6.1. This upgrade removes tablib’s dependency on MarkupPy in favour of ElementTree. If you export to HTML, then this change may affect your output format, particularly if you have already escaped HTML characters in the text.

This release fixes a regression introduced in v4. From v4.2, numeric, boolean and date/time widgets are written as native values to spreadsheet formats (ODS, XLS, XLSX). This was the default behavior in v3. See documentation.

This means that the coerce_to_string value which is passed to Widget is now ignored if you are exporting to a spreadsheet format from the Admin interface.

If you have subclassed Widget, Field or Resource, then you may need to adjust your code to include the **kwargs param as follows:

Widget.render(self, value, obj=None)

Widget.render(self, value, obj=None, **kwargs)

Field.export(self, instance)

Field.export(self, instance, **kwargs)

Resource.export_field(self, field, instance)

Resource.export_field(self, field, instance, **kwargs)

Resource.export_resource(self, instance, selected_fields=None)

Resource.export_resource(self, instance, selected_fields=None, **kwargs)

The Resource.get_fields() method is no longer called within the package and has been deprecated. If you have overridden this method then it should be removed.

v4 introduces significant updates to import-export. We have taken the opportunity to introduce breaking changes in order to fix some long-standing issues.

Refer to the changelog for more information. Please ensure you test thoroughly before deploying v4 to production.

This guide describes the major changes and how to upgrade.

We have modified installation methods to allow for optional dependencies. This means that you have to explicitly declare dependencies when installing import-export.

If you are not sure, or want to preserve the pre-v4 behaviour, then ensure that import-export is installed as follows (either in your requirements file or during installation):

Constructor arguments are dynamically set during instantiation based on the properties of the underlying Django db CharField. If the db field has blank set to True, then incoming values of empty strings or null are stored as empty strings. See CharWidget.

clean() will now return a string type as the default. The coerce_to_string option introduced in v3 is no longer used in this method.

The following widgets have had validation error messages updated:

We have standardized the export output which is returned from render().

Prior to v4, the export format returned from render() varied between Widget implementations. In v4, return values are rendered as strings by default (where applicable), with None values returned as empty strings. Widget params can modify this behavior.

This causes a change when exporting to Excel. In v3, certain fields, such as numeric values, were rendered as their native type. In v4, all fields are now rendered as strings. To preserve the v3 behavior when exporting to Excel, set the coerce_to_string param to False. See documentation.

Widget API documentation.

The ordering rules for exported fields has been standardized. See documentation.

If the raise_errors parameter of import_data() is True, then an instance of ImportError is raised. This exception wraps the underlying exception.

Prior to v4 we had numerous issues where users were confused when imports failed due to declared import_id_fields not being present in the dataset. We added functionality in v4 to check for this and to raise a clearer error message.

In some use-cases, it is a requirement that import_id_fields are not in the dataset, and are generated dynamically. If this affects your implementation, start with the documentation here.

The obj param passed to render() is deprecated. The render() method should not need to have a reference to model instance. The call to render() from export() has been removed.

Use of ExportViewFormMixin is deprecated. See this issue.

In the Admin UI, the declaration of resource_class is replaced by resource_classes:

LogEntry instances are created during import for creates, updates and deletes. The functionality to store LogEntry has changed in v4 in order to address a deprecation in Django 5. For this to work correctly, deleted instances are now always copied and retained in each RowResult so that they can be recorded in each LogEntry.

This only occurs for delete operations initiated from the Admin UI.

The export action has been updated to include the export workflow. Prior to v4, it was possible to select export selected items using an export admin action. However this meant that the export workflow was skipped and it was not possible to select the export resource. This has been fixed in v4 so that export workflow is now present when exporting via the Admin UI action. For more information see export documentation.

The export ‘confirm’ page now includes selectable fields for export. If you wish to revert to the previous (v3) version of the export confirm screen, add a export_form_class declaration to your Admin class subclass, for example:

The success message shown on successful import has been updated to include the number of ‘deleted’ and ‘skipped’ rows. See this PR.

The default error message for import errors has been modified to simplify the format. Error messages now contain the error message only by default. The row and traceback are not presented.

The original format can be restored by setting import_error_display on the Admin class definition. For example:

v4 of import-export contains a number of changes to the API. These changes are summarized in the table below. Refer to this PR for detailed information.

If you have customized import-export by overriding methods, then you may have to modify your installation before working with v4.

If you have not overridden any methods then you should not be affected by these changes and no changes to your code should be necessary.

The API changes include changes to method arguments, although some method names have changed.

Methods which process row data have been updated so that method args are standardized. This has been done to resolve inconsistency issues where the parameters differed between method calls, and to allow easier extensibility.

import_obj(self, obj, data, dry_run, **kwargs)

import_instance(self, instance, row, **kwargs)

obj param renamed to instance

data param renamed to row

dry_run param now in kwargs

after_import_instance(self, instance, new, row_number=None, **kwargs)

after_init_instance(self, instance, new, row, **kwargs)

row added as mandatory arg

row_number now in kwargs

This section describes methods in which the parameters have changed.

before_import(self, dataset, using_transactions, dry_run, **kwargs)

before_import(self, dataset, **kwargs)

using_transactions param now in kwargs

dry_run param now in kwargs

after_import(self, dataset, result, using_transactions, dry_run, **kwargs)

after_import(self, dataset, result, **kwargs)

using_transactions param now in kwargs

dry_run param now in kwargs

before_import_row(self, row, row_number=None, **kwargs)

before_import_row(self, row, **kwargs)

row_number now in kwargs

after_import_row(self, row, row_result, row_number=None, **kwargs)

after_import_row(self, row, row_result, **kwargs)

row_number now in kwargs

import_row(self, row, instance_loader, using_transactions=True, dry_run=False, **kwargs)

import_row(self, row, instance_loader, **kwargs)

dry_run param now in kwargs

using_transactions param now in kwargs

save_instance(self, instance, is_create, using_transactions=True, dry_run=False)

save_instance(self, instance, is_create, row, **kwargs)

dry_run param now in kwargs

using_transactions param now in kwargs

row added as mandatory arg

save_m2m(self, obj, data, using_transactions, dry_run)

save_m2m(self, instance, row, **kwargs)

row added as mandatory arg

obj renamed to instance

dry_run param now in kwargs

using_transactions param now in kwargs

before_save_instance(self, instance, using_transactions, dry_run)

before_save_instance(self, instance, row, **kwargs)

row added as mandatory arg

dry_run param now in kwargs

using_transactions param now in kwargs

after_save_instance(self, instance, using_transactions, dry_run)

after_save_instance(self, instance, row, **kwargs)

row added as mandatory arg

dry_run param now in kwargs

using_transactions param now in kwargs

delete_instance(self, instance, using_transactions=True, dry_run=False)

delete_instance(self, instance, row, **kwargs)

row added as mandatory arg

dry_run param now in kwargs

using_transactions param now in kwargs

before_delete_instance(self, instance, dry_run)

before_delete_instance(self, instance, row, **kwargs)

row added as mandatory arg

dry_run param now in kwargs

using_transactions param now in kwargs

after_delete_instance(self, instance, dry_run)

after_delete_instance(self, instance, row, **kwargs)

row added as mandatory arg

dry_run param now in kwargs

using_transactions param now in kwargs

import_field(self, field, obj, data, is_m2m=False, **kwargs)

import_field(self, field, instance, row, is_m2m=False, **kwargs):

obj renamed to instance

before_export(self, queryset, *args, **kwargs)

before_export(self, queryset, **kwargs)

unused *args list removed

after_export(self, queryset, data, *args, **kwargs)

after_export(self, queryset, dataset, **kwargs)

unused *args list removed

data renamed to dataset

filter_export(self, queryset, *args, **kwargs)

filter_export(self, queryset, **kwargs)

unused *args list removed

export_field(self, field, obj)

export_field(self, field, instance)

obj renamed to instance

export_resource(self, obj)

export_resource(self, instance, fields=None)

obj renamed to instance

fields passed as kwarg

export(self, *args, queryset=None, **kwargs)

export(self, queryset=None, **kwargs)

unused *args list removed

get_export_headers(self)

get_export_headers(self, fields=None)

fields passed as kwarg

get_resource_classes(self)

get_resource_classes(self, request)

get_resource_kwargs(self, request, *args, **kwargs)

get_resource_kwargs(self, request, **kwargs)

unused *args list removed

get_import_resource_kwargs(self, request, *args, **kwargs)

get_import_resource_kwargs(self, request, **kwargs)

unused *args list removed

get_import_resource_classes(self)

get_import_resource_classes(self, request)

choose_import_resource_class(self, form)

choose_import_resource_class(self, form, request)

get_export_resource_classes(self)

get_export_resource_classes(self, request)

get_export_resource_kwargs(self, request, *args, **kwargs)

get_export_resource_kwargs(self, request, **kwargs)

unused *args list removed

get_data_for_export(self, request, queryset, *args, **kwargs)

get_data_for_export(self, request, queryset, **kwargs)

unused *args list removed

choose_export_resource_class(self, form)

choose_export_resource_class(self, form, request)

clean(self, data, **kwargs)

clean(self, row, **kwargs)

get_value(self, instance)

obj renamed to instance

save(self, obj, data, is_m2m=False, **kwargs)

save(self, instance, row, is_m2m=False, **kwargs)

obj renamed to instance

export(self, instance)

obj renamed to instance

If you have subclassed one of the forms then you may need to modify the parameters passed to constructors.

The input_format field of ImportForm has been moved to the parent class (ImportExportFormBase) and renamed to format.

The file_format field of ExportForm has been removed and is now replaced by format.

__init__(self, *args, resources=None, **kwargs)

__init__(self, formats, resources, **kwargs)

formats added as a mandatory arg

resources added as a mandatory arg

unused *args list removed

---

## Django import / export — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/index.html

**Contents:**
- Django import / export

django-import-export is a Django application and library for importing and exporting data with included admin integration.

Import from / Export to multiple file formats

Manage import / export of object relations, data types

Handle create / update / delete / skip during imports

Support multiple formats (Excel, CSV, JSON, … and everything else that tablib supports)

Admin integration for importing / exporting

Preview import changes

Export data respecting admin filters

A screenshot of the change view with Import and Export buttons.

---

## Import workflow — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/import_workflow.html

**Contents:**
- Import workflow
- Transaction support

This document describes the import data workflow in detail, with hooks that enable customization of the import process.

Methods highlighted in yellow in the sequence diagram indicate public methods which can be overridden.

The import_data() method of Resource is responsible for importing data from a given dataset. Refer to the method documentation for parameters to this method.

This is what happens when the method is invoked:

First, a new Result instance, which holds errors and other information gathered during the import, is initialized.

Then, an BaseInstanceLoader responsible for loading existing instances is initialized. A different BaseInstanceLoader can be specified via ResourceOptions’s instance_loader_class attribute. A CachedInstanceLoader can be used to reduce number of database queries. See the instance_loaders for available implementations.

The before_import() hook is called. By implementing this method in your resource, you can customize the import process.

Each row of the to-be-imported dataset is processed according to the following steps:

The before_import_row() hook is called to allow for row data to be modified before it is imported.

get_or_init_instance() is called with current BaseInstanceLoader and current row of the dataset, returning an object and a Boolean declaring if the object is newly created or not.

If no object can be found for the current row, init_instance() is invoked to initialize an object.

As always, you can override the implementation of init_instance() to customize how the new object is created (i.e. set default values).

for_delete() is called to determine if the passed instance should be deleted. In this case, the import process for the current row is stopped at this point.

If the instance was not deleted in the previous step, import_row() is called with the instance as current object instance, row as current row.

import_field() is called for each field in Resource skipping many- to-many fields. Many-to-many fields are skipped because they require instances to have a primary key and therefore assignment is postponed to when the object has already been saved.

import_field() in turn calls save(), if Field.attribute is set and Field.column_name exists in the given row.

It then is determined whether the newly imported object is different from the already present object and if therefore the given row should be skipped or not. This is handled by calling skip_row() with original as the original object and instance as the current object from the dataset.

If the current row is to be skipped, row_result.import_type is set to IMPORT_TYPE_SKIP.

If the current row is not to be skipped, save_instance() is called and actually saves the instance when dry_run is not set.

There are two hook methods (that by default do nothing) giving you the option to customize the import process:

before_save_instance()

after_save_instance()

save_m2m() is called to save many to many fields.

RowResult is assigned with a diff between the original and the imported object fields, as well as and import_type attribute which states whether the row is new, updated, skipped or deleted.

If an exception is raised during row processing and import_row() was invoked with raise_errors=False (which is the default) the particular traceback is appended to RowResult as well.

If either the row was not skipped or the Resource is configured to report skipped rows, the RowResult is appended to the Result

The after_import_row() hook is called

The Result is returned.

If transaction support is enabled, whole import process is wrapped inside transaction and rolled back or committed respectively. All methods called from inside of import_data() (create / delete / update) receive False for dry_run argument.

---

## Testing — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/testing.html

**Contents:**
- Testing
- MySql / Postgres tests
- Coverage
- Bulk testing
  - Enable logging

All tests can be run using tox simply by running the tox command. By default, tests are run against a local sqlite2 instance. pyenv can be used to manage multiple python installations.

By using Docker, you can also run tests against either a MySQL db and/or Postgres.

The IMPORT_EXPORT_TEST_TYPE must be set according to the type of tests you wish to run. Set to ‘postgres’ for postgres tests, and ‘mysql-innodb’ for mysql tests. If this environment variable is blank (or is any other value) then the default sqlite2 db will be used.

This process is scripted in runtests.sh. Assuming that you have docker installed on your system, running runtests.sh will run tox against sqlite2, mysql and postgres. You can edit this script to customise testing as you wish.

Note that this is the process which is undertaken by CI builds.

Coverage data is written in parallel mode by default (defined in pyproject.toml).

A simple coverage report can be obtained with

However this may omit lines which are db specific. A full coverage report can be obtained by running tox.

After a tox run, you can view coverage data as follows:

Check the output of the above commands to locate the coverage HTML file.

There is a helper script available to generate and profile bulk loads. See scripts/bulk_import.py.

You can use this script by configuring environment variables as defined above, and then installing and running the test application. In order to run the helper script, you will need to install make install-test-requirements, and then add django-extensions to settings.py (INSTALLED_APPS).

You can then run the script as follows:

You can see console SQL debug logging by updating the LOGGING block in settings.py:

---

## Changelog — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/changelog.html

**Contents:**
- Changelog
- 5.0.0 (unreleased)
- 4.3.14 (2025-11-13)
- 4.3.13 (2025-10-31)
- 4.3.12 (2025-10-19)
- 4.3.11 (2025-10-19)
- 4.3.10 (2025-09-26)
- 4.3.9 (2025-07-21)
- 4.3.8 (2025-06-23)
- 4.3.7 (2025-02-25)

v5 introduces breaking changes and deprecations. Please refer to release notes.

Fixed issue where export forms were incorrectly showing import fields instead of export fields (2118)

Add support for Django 6.0, remove support for Python 3.9 (2112)

Fix Admin UI form field name collision for exports (2108)

Removed the deprecated get_valid_export_item_pks() method in favour of get_queryset() (1898)

Add Ukrainian translation (2132)

Fix: file_name is None in before_import_row when skip_import_confirm=True (2129)

Minor documentation fix

Fix for export not retaining URI query params (2097)

Improved field value extraction for dict-based querysets (2098)

Performance improvements for membership checks (2090)

Fix ForeignKeyWidget export issue (2117)

Improved documentation for clean() methods (2115)

Documentation updates: JSONField export with attribute syntax (2100)

Documentation updates: handling TooManyFieldsSent (2103)

Updated Turkish translation (2101)

Updated Czech translation (2111)

Allow specifying meta options in the model_resourcefactory (2078)

Allow custom fields and methods in model_resourcefactory (2081)

FAQ update to describe how to customize Excel exports (2088)

ui: fix error display twice issue on export field select page (2066)

ui: add ‘select all’ fields toggle on export page (2068)

Add Hebrew translation (2071)

ui: fix display of non field errors on import (2075)

Update French translation (2042)

Add flag to ignore empty rows in XLSX import (2028)

Add support for Django 5.2 (2037)

Fix Chinese translation (2040)

Clarify documentation on creating non-existent relations (2029)

Update Turkish translations (2031)

Handle QuerySets called with values() on export (2011)

Update all translations (2014)

Updated Farsi translation (2008)

Updated German translation (2012)

Fix imports for openpyxl (2005)

Addition of import & export management commands (1992)

Handle IllegalCharacterError in xlsx exports (2001)

Add __repr__ method to InvalidRow for improved debugging (2003)

Removed dependency files in favour of pyproject.toml (1982)

Documentation updates (1989)

Fix crash on export of tz-aware datetime to binary formats (1995)

This release contains breaking changes. Please refer to release notes.

Upgraded tablib version (1627)

Document overriding formats (1868)

Consistent queryset creation in ModelAdmin export mixin (1890)

Deprecated get_valid_export_item_pks() in favour of get_queryset() (1890)

Improve deprecation warning for ExportViewFormMixin to report at point of class definition (1900)

Fix export for fields with custom declared name (1903)

Hide the “Resource” form when it only has one option (1908)

Update date, time and datetime widget render method to handle derived instance (1918)

Add support for Django 5.1 (1926)

Accept numbers using the numeric separators of the current language in number widgets (FloatWidget(), IntegerWidget(), DecimalWidget()) (1927)

Added warning for declared fields excluded from fields whitelist (1930)

Fix v3 regression: handle native types on export to spreadsheet (1939)

Fix export button displayed on change screen when export permission not assigned (1942)

Fix crash for Django 5.1 when rows are skipped (1944)

Allow callable in dehydrate method (1950)

Fix crash when Resource fields declared incorrectly (1963)

Updated dependencies (1979)

Restore return value for deprecated method get_fields() (1897)

Improve Error class (1882)

Fix response content assertions (1883)

Admin UI: display checkboxes before labels in export form (1884)

deprecated unused method: get_fields() (1885)

remove django version check for custom storages (1889)

docs: clarify for_delete() documentation (1877)

fix default Field returns empty string instead of ‘None’ (1872)

revert setting default value for attribute (1875)

docs: clarify widget configuration (1865)

Enable skip export confirm page (1867)

fix documentation to show correct method for reading form data on export (1859)

Admin UI: display both field name and column name on export (1857)

fix export declared field with custom column name (1861)

fix declared fields do not have correct Widget class set (1861)

docs: clarify changes to CharWidget in v4 (1862)

refactor Resource to remove code duplication in export (1863)

Added additional test for export field order (1848)

fix crash on import when relation has custom PK (1853)

fix crash on export from action when instance has custom PK (1854)

Fix for invalid build due to malformed README.rst (1851)

Refactored DateWidget & DateTimeWidget to remove code duplication (1839)

Release note documentation updated (1840)

Added missing migration to example app (1843)

Fix admin UI display of field import order (1849)

Support widgets with CSS and JS media in ImportForm (1807)

Documentation updates (1833)

Clarified documentation when importing with import_id_fields (1836)

re-add resource_class deprecation warning (1837)

fixed Arabic translation for ‘import’ word (1838)

fix export with custom column name (1821)

fix allow column_name to be declared in fields list (1822)

fix clash between key_is_id and use_natural_foreign_keys (1824)

remove unreachable code (1825)

fix issue with widget assignment for custom ForeignKey subclasses (1826)

performance: select of valid pks for export restricted to action exports (1827)

fix crash on export with custom column name (1828)

remove outdated datetime formatting logic (1830)

fix crash on export when model has no id (1802)

fix Widget crash when django Field subclass is used (1805)

fix regression: allow imports when default import_id_field is not present (1813)

Removed v3 deprecations (1629)

Deprecation of ExportViewFormMixin (1666)

Refactor ordering logic (1626)

Refactor ‘diff’ logic to avoid calling dehydrate methods

Refactor declarations of fields, import_order and export_order to fix ordering issues

refactor to export HTML / formulae escaping updates (1638)

removed unused variable Result.new_record (1640)

Refactor resources.py to standardise method args (1641)

added specific check for missing import_id_fields (1645)

Enable optional tablib dependencies (1647)

added get_lookup_kwargs() to make it easier to override object lookup (1651)

Standardised interface of render() (1657)

Fix declaring existing model field(s) in ModelResource altering export order (1663)

Added do_instance_save() helper method (1668)

Enable defining Resource model as a string (1669)

Support multiple Resources for export (1671)

Support export from model change form (1687)

Import form defaults to read-only field if only one format defined (1690)

Updated Admin UI to track deleted and skipped Imports (1691)

Added customizable MediaStorage (1708)

Added customization of Admin UI import error messages (1727)

Improve output of error messages (1729)

Added feature: selectable fields for admin export view (1734)

Added specific check for declared import_id_fields not in dataset (1735)

added try / catch to add_instance_info() to handle unserializable instances (1767)

Add form error if source file contains invalid header (1780)

Remove unneeded format method overrides (1785)

Support dynamic selection of Resource class based on request property (1787)

dynamic widget parameters for CharField fixes ‘NOT NULL constraint’ error in xlsx (1485)

fix cooperation with adminsortable2 (1633)

Removed unused method utils.original()

Fix deprecated log_action method (1673)

fix multiple inheritance not setting options (1696)

Fix issue where declared Resource fields not defined in fields are still imported (1702)

Fixed handling of FieldError during Admin import (1755)

Fixed handling of django FieldError during Admin export (1756)

Add check for type to render() (1757)

fix: YAML export does not work with SafeString (1762)

fix: render() crashes if value is None (1771)

fix form not being passed to get_import_resource_kwargs() (1789)

Fix: Missing default widget for PositiveBigIntegerField (1795)

Refactor build process (1630)

Refactored test_admin_integration(): split into smaller test modules (1662)

Refactored test_resources(): split into smaller test modules (1672)

Updated docker-compose command with latest version syntax in runtests.sh (1686)

Refactored resources into separate modules for declarative and options (1695)

Refactored tests to remove dependencies between tests (1703)

Handle python3.12 datetime deprecations (1705)

Refactor test_resources.py into smaller modules (1733)

Updated test coverage to include error row when collect_failed_rows is True (1753)

Removed support for django 3.2 (1790)

Added test for widgets generating by model fields 1795)

Clarified skip_diff documentation (1655)

Improved documentation relating to validation on import (1665)

Added FAQ entry for exporting large datasets (1706)

Relocated admin integration section from advanced_usage.rst into new file (1713)

Updated Admin integration documentation to clarify how to save custom form values (1746)

Fix slow export with ForeignKey id (1717)

updated translations for release-4 (1775)

Update translations for Russian language (1797)

Add additional django template block for extending import page (1776)

Pass get_export_resource_kwargs() to Resource constructor export_action() (1739)

Fix issue with model class passed to Resource constructor crashing on export (1745)

Fix indentation for skip_row docstring (1743)

Return kwargs by default from get_resource_kwargs() (1748)

Fix issue with highlight when using ‘light’ color scheme (1728)

Remove unnecessary ChangeList queries to speed up export via Admin UI (1715)

Respect color scheme override (1720)

Update FAQ to cover skipping rows with validation errors (1721)

Added support for django5 (1634)

Show list of exported fields in Admin UI (1685)

Added CONTRIBUTING.md

Added support for python 3.12 (1698)

Update Finnish translations (1701)

export_admin_action() can be overridden by subclassing it in the ModelAdmin (1681)

Updated Spanish translations (1639)

Added documentation and tests for retrieving instance information after import (1643)

render() returns None as empty string if coerce_to_string is True (1650)

Updated documentation to describe how to select for export in Admin UI (1670)

Added catch for django5 deprecation warning (1676)

Updated and compiled message files (1678)

Added .readthedocs.yaml (1625)

Remove ‘escape output’ deprecation (1618)

Removal of deprecated IMPORT_EXPORT_ESCAPE_OUTPUT_ON_EXPORT.

Deprecation of IMPORT_EXPORT_ESCAPE_HTML_ON_EXPORT. Refer to installation docs.

Refactoring and fix to support filtering exports (1579)

Store instance and original object in RowResult (1584)

Add customizable blocks in import.html (1598)

Include ‘allowed formats’ settings (1606)

Add kwargs to enable CharWidget to return values as strings (1623)

Add Finnish translation (1588)

Updated ru translation (1604)

Fixed badly formatted translation string (1622)

Remove ‘escape output’ deprecation (1618)

Do not decode bytes when writing to MediaStorage (1615)

Fix for cache entries not removed (1621)

Added support for Django 4.2 (1570)

Add automatic formatting and linting (1571)

removed duplicate admin integration tests (1616)

Removed support for python3.7 and django4.0 (past EOL) (1618)

Updated documentation for interoperability with third party libraries (1614)

Escape formulae on export to XLSX (1568)

This includes deprecation of IMPORT_EXPORT_ESCAPE_OUTPUT_ON_EXPORT.

Refer to installation for alternatives.

import_export.formats.TablibFormat.export(): escape_output flag now deprecated in favour of escape_html and escape_formulae.

Refactor methods so that args are declared correctly (1566)

This includes deprecations to be aware of if you have overridden export() or ImportExportFormBase.

export(): If passing queryset as the first arg, ensure this is passed as a named parameter.

ImportExportFormBase: If passing resources to __init__ as the first arg, ensure this is passed as a named parameter.

Updated setup.py (1564)

Added SECURITY.md (1563)

Updated FAQ to include workaround for RelatedObjectDoesNotExist exception (1562)

Prevent error comparing m2m field of the new objects (1560)

Add documentation for passing data from admin form to Resource (1555)

Added new translations to Spanish and Spanish (Argentina) (1552)

Pass kwargs to import_set function (1448)

Float and Decimal widgets use LANGUAGE_CODE on export (1501)

Add optional dehydrate method param (1536)

exceptions module has been undeprecated

Updated DE translation (1537)

Add option for single step import via Admin Site (1540)

Add support for m2m add (1545)

collect errors on bulk operations (1541)

this change causes bulk import errors to be logged at DEBUG level not EXCEPTION.

Improve bulk import performance (1539)

raise_errors has been deprecated as a kwarg in import_row()

Reduce memory footprint during import (1542)

documentation updates (1533)

add detailed format parameter docstrings to DateWidget and TimeWidget (1532)

fix xss vulnerability in html export (1546)

Support Python 3.11 (1508)

use get_list_select_related in ExportMixin (1511)

bugfix: handle crash on start-up when change_list_template is a property (1523)

bugfix: include instance info in row result when row is skipped (1526)

bugfix: add **kwargs param to Resource constructor (1527)

Updated django-import-export-ci.yml to fix node.js deprecation

bugfix: DateTimeWidget.clean() handles tz aware datetime (1499)

Updated translations for v3.0.0 release (1500)

This release makes some minor changes to the public API. If you have overridden any methods from the resources or widgets modules, you may need to update your implementation to accommodate these changes.

This fixes an issue where ManyToMany fields are not checked correctly in skip_row(). This means that skip_row() now takes row as a mandatory arg. If you have overridden skip_row() in your own implementation, you will need to add row as an arg.

If you have overridden skip_row() you can choose whether or not to skip rows if validation errors are present. The default behavior is to not to skip rows if there are validation errors during import.

import_export.resources.save_instance() now takes an additional mandatory argument: is_create. If you have overridden save_instance() in your own code, you will need to add this new argument.

If you have overridden clean() then you should update your method definition to reflect this change.

widgets.ForeignKeyWidget / widgets.ManyToManyWidget: The unused *args param has been removed from __init__(). If you have overridden ForeignKeyWidget or ManyToManyWidget you may need to update your implementation to reflect this change.

Exceptions raised during the import process are now presented as form errors, instead of being wrapped in a <H1> tag in the response. If you have any custom logic which uses the error written directly into the response, then this may need to be changed.

Previous ImportForm implementation was based on Django’s forms.Form, if you have any custom ImportForm you now need to inherit from import_export.forms.ImportExportFormBase.

If you are using admin mixins from this library in conjunction with code that overrides change_list_template (typically admin mixins from other libraries such as django-admin-sortable2 or reversion), object tools in the admin change list views may render differently now.

If you have created a custom template which extends any import_export template, then this may now cause a recursion error (see `1415 <https://github.com/django-import-export/django-import-export/pull/1415 >`_)

If you have made customizations to the import template then you may need to refactor these after the addition of block declarations.

This release adds some deprecations which will be removed in a future release.

Add support for multiple resources in ModelAdmin. (1223)

The *Mixin.resource_class accepting single resource has been deprecated and the new *Mixin.resource_classes accepting subscriptable type (list, tuple, …) has been added.

Same applies to all of the get_resource_class, get_import_resource_class and get_export_resource_class methods.

Deprecated exceptions.py (1372)

Refactored form-related methods on ImportMixin / ExportMixin (1147)

The following are deprecated:

get_confirm_import_form()

Default format selections set correctly for export action (1389)

Added option to store raw row values in each row’s RowResult (1393)

Add natural key support to ForeignKeyWidget (1371)

Optimised default instantiation of CharWidget (1414)

Allow custom change_list_template in admin views using mixins (1483)

Added blocks to import template (1488)

improve compatibility with previous ImportForm signature (1434)

Refactored form-related methods on ImportMixin / ExportMixin (1147)

Include custom form media in templates (1038)

Remove unnecessary files generated when running tox locally (1426)

Fixed Makefile coverage: added coverage combine

Fixed handling of LF character when using CacheStorage (1417)

bugfix: skip_row() handles M2M field when UUID pk used

Fix broken link to tablib formats page (1418)

Fix broken image ref in README.rst

bugfix: skip_row() fix crash when model has m2m field and none is provided in upload (1439)

Fix deprecation in example application: Added support for transitional form renderer (1451)

Increased test coverage, refactored CI build to use tox (1372)

Clarified issues around the usage of temporary storage (1306)

Fix deprecation in example application: Added support for transitional form renderer (1451)

Escape HTML output when rendering decoding errors (1469)

Apply make_aware when the original file contains actual datetimes (1478)

Automatically guess the format of the file when importing (1460)

Updated import.css to support dark mode (1318)

Fix crash when import_data() called with empty Dataset and collect_failed_rows=True (1381)

Improve Korean translation (1402)

Update example subclass widget code (1407)

Drop support for python3.6, django 2.2, 3.0, 3.1 (1408)

Add get_export_form() to ExportMixin (1409)

Removed django_extensions from example app settings (1356)

Added support for Django 4.0 (1357)

Big integer support for Integer widget (788)

Run compilemessages command to keep .mo files in sync (1299)

Added skip_html_diff meta attribute (1329)

Added python3.10 to tox and CI environment list (1336)

Add ability to rollback the import on validation error (1339)

Fix missing migration on example app (1346)

Fix crash when deleting via admin site (1347)

Use Github secret in CI script instead of hard-coded password (1348)

Documentation: correct error in example application which leads to crash (1353)

Revert ‘dark mode’ css: causes issues in django2.2 (1330)

Added guard for null ‘options’ to fix crash (1325)

Updated import.css to support dark mode (1323)

Fixed regression where overridden mixin methods are not called (1315)

Fix xls/xlsx import of Time fields (1314)

Added support for ‘to_encoding’ attribute (1311)

Removed travis and replaced with github actions for CI (1307)

Increased test coverage (1286)

Fix minor date formatting issue for date with years < 1000 (1285)

Translate the zh_Hans missing part (1279)

Remove code duplication from mixins.py and admin.py (1277)

Fix example in BooleanWidget docs (1276)

Better support for Django main (1272)

don’t test Django main branch with python36,37 (1269)

Support Django 3.2 (1265)

Correct typo in Readme (1258)

Rephrase logical clauses in docstrings (1255)

Support multiple databases (1254)

Update django master to django main (1251)

Add Farsi translated messages in the locale (1249)

Update Russian translations (1244)

Append export admin action using ModelAdmin.get_actions (1241)

Fix minor mistake in makemigrations command (1233)

Remove EOL Python 3.5 from CI (1228)

CachedInstanceLoader defaults to empty when import_id is missing (1225)

Add kwargs to import_row, import_object and import_field (1190)

Call load_workbook() with data_only flag (1095)

Changed the default value for IMPORT_EXPORT_CHUNK_SIZE to 100. (1196)

Add translation for Korean (1218)

Update linting, CI, and docs.

Fix deprecated Django 3.1 Signal(providing_args=...) usage.

Fix deprecated Django 3.1 django.conf.urls.url() usage.

Add missing translation keys for all languages (1144)

Added missing Portuguese translations (1145)

Add kazakh translations (1161)

Add bulk operations (1149)

Deal with importing a BooleanField that actually has True, False, and None values. (1071)

Add row_number parameter to before_import_row, after_import_row and after_import_instance (1040)

Paginate queryset if Queryset.prefetch_related is used (1050)

Fix DurationWidget handling of zero value (1117)

Make import diff view only show headers for user visible fields (1109)

Make confirm_form accessible in get_import_resource_kwargs and get_import_data_kwargs (994, 1108)

Initialize Decimal with text value, fix #1035 (1039)

Adds meta flag ‘skip_diff’ to enable skipping of diff operations (1045)

Update docs (1097, 1114, 1122, 969, 1083, 1093)

Add support for tablib >= 1.0 (1061)

Add ability to install a subset of tablib supported formats and save some automatic dependency installations (needs tablib >= 1.0)

Use column_name when checking row for fields (1056)

Fix deprecated Django 3.0 function usage (1054)

Pin tablib version to not use new major version (1063)

Format field is always shown on Django 2.2 (1007)

Removed support for Django < 2.0

Removed support for Python < 3.5

feat: Support for Postgres JSONb Field (904)

feat: Better surfacing of validation errors in UI / optional model instance validation (852)

chore: Use modern setuptools in setup.py (862)

chore: Update URLs to use https:// (863)

chore: remove outdated workarounds

chore: Run SQLite tests with in-memory database

fix: Change logging level (832)

fix: Changed get_instance() return val (842)

fix: Django2.1 ImportExportModelAdmin export (797, 819)

setup: add django2.1 to test matrix

JSONWidget for jsonb fields (803)

Add ExportActionMixin (809)

Add Import Export Permissioning #608 (804)

write_to_tmp_storage() for import_action() (781)

follow relationships on ForeignKeyWidget (798)

Update all pypi.python.org URLs to pypi.org

added test for tsv import

added unicode support for TSV for python 2

Added ExportViewMixin (692)

Make deep copy of fields from class attr to instance attr (550)

Fix #612: NumberWidget.is_empty() should strip the value if string type (613)

Fix #713: last day isn’t included in results qs (779)

use Python3 compatible MySql driver in development (706)

fix: warning U mode is deprecated in python 3 (776)

refactor: easier overriding widgets and default field (769)

Updated documentation regarding declaring fields (735)

custom js for action form also handles grappelli (719)

Use ‘verbose_name’ in breadcrumbs to match Django default (732)

Add Resource.get_diff_class() (745)

Fix and add polish translation (747)

Restore raise_errors to before_import (749)

Switch to semver versioning (687)

Require Django>=1.8 (685)

upgrade tox configuration (737)

skip_row override example (702)

Testing against Django 2.0 should not fail (709)

Refactor transaction handling (690)

Resolves #703 fields shadowed (703)

discourage installation as a zipped egg (548)

Fixed middleware settings in test app for Django 2.x (696)

Refactors and optimizations (686, 632, 684, 636, 631, 629, 635, 683)

Travis tests for Django 2.0.x (691)

Refactor import_row call by using keyword arguments (585)

Added {{ block.super }} call in block bodyclass in admin/base_site.html (582)

Add support for the Django DurationField with DurationWidget (575)

GitHub bmihelac -> django-import-export Account Update (574)

Add intersphinx links to documentation (572)

Add Resource.get_import_fields() (569)

Fixed readme mistake (568)

Bugfix/fix m2m widget clean (515)

Allow injection of context data for template rendered by import_action() and export_action() (544)

Bugfix/fix exception in generate_log_entries() (543)

Process import dataset and result in separate methods (542)

Bugfix/fix error in converting exceptions to strings (526)

Fix admin integration tests for the new “Import finished…” message, update Czech translations to 100% coverage. (596)

Make import form type easier to override (604)

Add saves_null_values attribute to Field to control whether null values are saved on the object (611)

Add Bulgarian translations (656)

Add django 1.11 to TravisCI (621)

Make Signals code example format correctly in documentation (553)

Add Django as requirement to setup.py (634)

Update import of reverse for django 2.x (620)

Add Django-version classifiers to setup.py’s CLASSIFIERS (616)

Some fixes for Django 2.0 (672)

Strip whitespace when looking up ManyToMany fields (668)

Fix all ResourceWarnings during tests in Python 3.x (637)

Remove downloads count badge from README since shields.io no longer supports it for PyPi (677)

Add coveralls support and README badge (678)

French locale not in pypi (524)

Bugfix/fix undefined template variables (519)

Hide default value in diff when importing a new instance (458)

Append rows to Result object via function call to allow overriding (462)

Add get_resource_kwargs to allow passing request to resource (457)

Expose Django user to get_export_data() and export() (447)

Add before_export and after_export hooks (449)

fire events post_import, post_export events (440)

add **kwargs to export_data / create_dataset

Add before_import_row() and after_import_row() (452)

Add get_export_fields() to Resource to control what fields are exported (461)

Control user-visible fields (466)

Fix diff for models using ManyRelatedManager

Handle already cleaned objects (484)

Add after_import_instance hook (489)

Use optimized xlsx reader (482)

Adds resource_class of BookResource (re-adds) in admin docs (481)

Require POST method for process_import() (478)

Add SimpleArrayWidget to support use of django.contrib.postgres.fields.ArrayField (472)

Add new Diff class (477)

Fix #375: add row to widget.clean(), obj to widget.render() (479)

Restore transactions for data import (480)

Refactor the import-export templates (496)

Update doc links to the stable version, update rtfd to .io (507)

Fixed typo in the Czech translation (495)

Add FloatWidget, use with model fields models.FloatField (433)

Fix default values in fields (431, 364)

Field constructor default argument is NOT_PROVIDED instead of None Field clean method checks value against Field.empty_values [None, ‘’]

FIX: No static/ when installed via pip (427)

Add total # of imports and total # of updates to import success msg

fix MediaStorage does not respect the read_mode parameter (416)

Reset SQL sequences when new objects are imported (59)

Let Resource rollback if import throws exception (377)

Fixes error when a single value is stored in m2m relation field (177)

Add support for django.db.models.TimeField (381)

add xlsx import support

fix for fields with a dyanmic default callable (360)

Add Django 1.9 support

Django 1.4 is not supported (348)

FIX: importing csv in python 3

FIX: importing csv UnicodeEncodeError introduced in 0.2.9 (347)

Allow Field.save() relation following (344)

Support default values on fields (and models) (345)

m2m widget: allow trailing comma (343)

Open csv files as text and not binary (127)

use the IntegerWidget for database-fields of type BigIntegerField (302)

make datetime timezone aware if USE_TZ is True (283).

Fix 0 is interpreted as None in number widgets (274)

add possibility to override tmp storage class (133, 251)

better error reporting (259)

Django 1.8 compatibility

add attribute inheritance to Resource (140)

make the filename and user available to import_data (237)

Add to_encoding functionality (244)

Call before_import before creating the instance_loader - fixes (193)

added use of get_diff_headers method into import.html template (158)

Try to use OrderedDict instead of SortedDict, which is deprecated in Django 1.7 (157)

fixed #105 unicode import

remove invalid form action “form_url” (154)

Do not convert numeric types to string (149)

implement export as an admin action (124)

fix: get_value raised attribute error on model method call

Fixed XLS import on python 3. Optimized loop

Fixed properly skipping row marked as skipped when importing data from the admin interface.

Allow Resource.export to accept iterables as well as querysets

Improve error messages

FIX: Properly handle NullBoleanField (115) - Backward Incompatible Change previously None values were handled as false

Add separator and field keyword arguments to ManyToManyWidget

FIX: No support for dates before 1900 (93)

RowResult now stores exception object rather than it’s repr

Admin integration - add EntryLog object for each added/updated/deleted instance

FIX import_file_name form field can be use to access the filesystem (65)

Additional hooks for customizing the workflow (61)

Prevent queryset caching when exporting (44)

Allow unchanged rows to be skipped when importing (30)

Update tests for Django 1.6 (57)

Allow different ResourceClass to be used in ImportExportModelAdmin (49)

Use field_name instead of column_name for field dehydration, FIX (36)

Handle OneToOneField, FIX (17) - Exception when attempting access something on the related_name.

export filter not working (23)

DB transactions support for importing data

support for deleting objects during import

Allowing a field to be ‘dehydrated’ with a custom method

added ExportForm to admin integration for choosing export file format

refactor admin integration to allow better handling of specific formats supported features and better handling of reading text files

include all available formats in Admin integration

---

## Django Management Commands — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/management_commands.html

**Contents:**
- Django Management Commands
- Export Command
- Usage
- Example
- Import Command
- Usage
- Example

The export command allows you to export data from a specified Django model or a resource class. The exported data can be saved in different formats, such as CSV or XLSX.

format: Specify the format in which the data should be exported. -

resource: Specify the resource or model to export. Accepts a resource class or a model class in dotted path format. - –encoding (optional): Specify the encoding (e.g., ‘utf-8’) to be used for the exported data.

This command will export the User model data in CSV format using utf-8 encoding.

This command will export the data from MyResource resource in XLSX format.

The import command allows you to import data from a file using a specified Django model or a custom resource class.

resource: The resource class or model class in dotted path format.

import_file_name: The file from which data is imported (- can be used to indicate stdin).

–format (optional): Specify the format of the data to import. If not provided, it will be guessed from the mimetype.

–encoding (optional): Specify the character encoding of the data.

–dry-run: Perform a trial run without making changes.

–raise-errors: Raise any encountered errors during execution.

Import data from file into auth.User model using default model resource:

Import data from file using custom model resource, raising errors:

---

## Installation and configuration — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/installation.html

**Contents:**
- Installation and configuration
- Settings
  - IMPORT_EXPORT_USE_TRANSACTIONS
  - IMPORT_EXPORT_SKIP_ADMIN_LOG
  - IMPORT_EXPORT_TMP_STORAGE_CLASS
  - IMPORT_EXPORT_DEFAULT_FILE_STORAGE
  - IMPORT_EXPORT_IMPORT_PERMISSION_CODE
  - IMPORT_EXPORT_EXPORT_PERMISSION_CODE
  - IMPORT_EXPORT_CHUNK_SIZE
  - IMPORT_EXPORT_SKIP_ADMIN_CONFIRM

import-export is available on the Python Package Index (PyPI), so it can be installed with standard Python tools like pip or easy_install:

This will automatically install the default formats supported by tablib. If you need additional formats you should install the extra dependencies as required appropriate tablib dependencies (e.g. pip install django-import-export[xlsx]).

To install all available formats, use pip install django-import-export[all].

For all formats, see the tablib documentation.

Alternatively, you can install the git repository directly to obtain the development version:

Now, you’re good to go, unless you want to use import-export from the admin as well. In this case, you need to add it to your INSTALLED_APPS and let Django collect its static files.

All prerequisites are set up! See Getting started to learn how to use import-export in your project.

You can configure the following in your settings file:

Controls if resource importing should use database transactions. Defaults to True. Using transactions makes imports safer as a failure during import won’t import only part of the data set.

Can be overridden on a Resource class by setting the use_transactions class attribute.

If set to True, skips the creation of admin log entries when importing via the Admin UI. Defaults to False. This can speed up importing large data sets, at the cost of losing an audit trail.

Can be overridden on a ModelAdmin class inheriting from ImportMixin by setting the skip_admin_log class attribute.

A string path to the preferred temporary storage module.

Controls which storage class to use for storing the temporary uploaded file during imports. Defaults to import_export.tmp_storages.TempFolderStorage.

Can be overridden on a ModelAdmin class inheriting from ImportMixin by setting the tmp_storage_class class attribute.

A string path to a customized storage implementation.

This setting is deprecated and only applies if using Django with a version less than 4.2, and will be removed in a future release.

If set, lists the permission code that is required for users to perform the ‘import’ action. Defaults to None, which means all users can perform imports.

Django’s built-in permissions have the codes add, change, delete, and view. You can also add your own permissions. For example, if you set this value to ‘import’, then you can define an explicit permission for import in the example app with:

Now only users who are assigned ‘import_book’ permission will be able to perform imports. For more information refer to the Django auth documentation.

Defines the same behaviour as IMPORT_EXPORT_IMPORT_PERMISSION_CODE, but for export.

An integer that defines the size of chunks when iterating a QuerySet for data exports. Defaults to 100. You may be able to save memory usage by decreasing it, or speed up exports by increasing it.

Can be overridden on a Resource class by setting the chunk_size class attribute.

If True, no import confirmation page will be presented to the user in the Admin UI. The file will be imported in a single step.

By default, the import will occur in a transaction. If the import causes any runtime errors (including validation errors), then the errors are presented to the user and then entire transaction is rolled back.

Note that if you disable transaction support via configuration (or if your database does not support transactions), then validation errors will still be presented to the user but valid rows will have imported.

This flag can be enabled for the model admin using the skip_import_confirm flag.

A boolean value which will skip the export form in the Admin UI, when the export is initiated from the change list page. The file will be exported in a single step.

the first element in the resource_classes list will be used.

the first element in the EXPORT_FORMATS list will be used.

This flag can be enabled for the model admin using the skip_export_form flag.

A boolean value which will skip the export form in the Admin UI, but only when the export is requested from an Admin UI action, or from the ‘Export’ button on the change form.

See also IMPORT_EXPORT_SKIP_ADMIN_EXPORT_UI.

This flag can be enabled for the model admin using the skip_export_form_from_action flag.

If set to True, strings will be sanitized by removing any leading ‘=’ character. This is to prevent execution of Excel formulae. By default this is False.

If an export to XLSX format generates IllegalCharacterError, then if this flag is True strings will be sanitized by removing any invalid Excel characters, replacing them with the unicode replacement character. By default this is False, meaning that IllegalCharacterError is caught and re-raised as ValueError.

A list that defines which file formats will be allowed during imports and exports. Defaults to import_export.formats.base_formats.DEFAULT_FORMATS. The values must be those provided in import_export.formats.base_formats e.g

This can be set for a specific model admin by declaring the formats attribute.

A list that defines which file formats will be allowed during imports. Defaults to IMPORT_EXPORT_FORMATS. The values must be those provided in import_export.formats.base_formats e.g

This can be set for a specific model admin by declaring the import_formats attribute.

A list that defines which file formats will be allowed during exports. Defaults to IMPORT_EXPORT_FORMATS. The values must be those provided in import_export.formats.base_formats e.g

This can be set for a specific model admin by declaring the export_formats attribute.

If set to True, rows without content will be ignored in XSLX imports. This prevents an old Excel 1.0 bug which causes openpyxl max_rows to be counting all logical empty rows. Some editors (like LibreOffice) might add \(2^{20}\) empty rows to the file, which causes a significant slowdown. By default this is False.

There’s an example application that showcases what import_export can do.

Before starting, set up a virtual environment (“venv”) using these instructions.

You can initialize and run the example application as follows:

Go to http://127.0.0.1:8000

For example import files, see Test data.

You can adjust the log level to see output as required. This is an example configuration to be placed in your application settings:

---

## Screenshots — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/screenshots.html

**Contents:**
- Screenshots

These are some screenshots for the Admin UI of the example application.

Shows the initial import form with fields for selecting the resource, file and format.

Shows the confirmation page which appears prior to committing the import to the database.

Shows the confirmation page on successful import.

Shows the preview page for updating existing records with author details.

Shows selecting records for export.

Shows the export form with fields for selecting the resource, fields and format.

---

## Getting started — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/getting_started.html

**Contents:**
- Getting started
- Introduction
- Test data
- The test models
- Creating a resource
- Importing data
  - Deleting data
- Exporting data

This section describes how to get started with import-export. We’ll use the example application as a guide.

import-export can be used programmatically as described here, or it can be integrated with the Django Admin interface.

There are sample files which can be used to test importing data in the tests/core/exports directory.

For example purposes, we’ll use a simplified book app. Here is our models.py:

To integrate import-export with our Book model, we will create a ModelResource class in admin.py that will describe how this resource can be imported or exported:

Let’s import some data!

In the fourth line we use modelresource_factory() to create a default ModelResource. The ModelResource class created this way is equal to the one shown in the example in section Creating a resource. For more advanced usage of this function, see Using modelresource_factory.

In fifth line a Dataset with columns id and name, and one book entry, are created. A field (or combination of fields) which uniquely identifies an instance always needs to be present. This is so that the import process can manage creates / updates. In this case, we use id. For more information, see Create or update model instances.

In the rest of the code we first pretend to import data using import_data() and dry_run set, then check for any errors and actually import data this time.

for a detailed description of the import workflow and its customization options.

To delete objects during import, implement the for_delete() method on your Resource class. You should add custom logic which will signify which rows are to be deleted.

For example, suppose you would like to have a field in the import dataset to indicate which rows should be deleted. You could include a field called delete which has either a 1 or 0 value.

In this case, declare the resource as follows:

If the delete flag is set on a ‘new’ instance (i.e. the row does not already exist in the db) then the row will be skipped.

Now that we have defined a ModelResource class, we can export books:

Data exported programmatically is not sanitized for malicious content. You will need to understand the implications of this and handle accordingly. See Security.

---

## Using celery — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/celery.html

**Contents:**
- Using celery

You can use one of the third-party applications to process long imports and exports in Celery:

django-import-export-celery (PyPI)

django-import-export-extensions (PyPI)

---

## Contributing — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/contributing.html

**Contents:**
- Contributing
- Philosophy
- Questions
- Guidelines For Reporting An Issue/Feature
- Guidelines For Contributing Code
- Development
  - Formatting
  - Create virtual environment
  - Run tests
  - Build documentation

django-import-export is open-source and, as such, grows (or shrinks) & improves in part due to the community. Below are some guidelines on how to help with the project.

By contributing you agree to abide by the Code of Conduct.

django-import-export is BSD-licensed. All contributed code must be either

the original work of the author, contributed under the BSD, or…

work taken from another project released under a BSD-compatible license.

GPL’d (or similar) works are not eligible for inclusion.

django-import-export’s git main branch should always be stable, production-ready & passing all tests.

Please check the common issues section of the FAQ to see if your question already has an answer.

For general questions about usage, we recommend posting to Stack Overflow, using the django-import-export tag. Please search existing answers to see if any match your problem. If not, post a new question including as much relevant detail as you can. See how to ask for more details.

For questions about the internals of the library, please raise an issue and use the ‘question’ workflow.

First check to see if there is an existing issue which answers your question.

Remember to include as much detail as you can so that your question is answered in a timely manner.

So you’ve found a bug or have a great idea for a feature. Here are the steps you should take to help get it added/fixed in django-import-export:

First, check to see if there’s an existing issue or pull request for the bug/feature.

If there isn’t one there, please file an issue. The ideal report includes:

A description of the problem/suggestion.

How to recreate the bug.

If relevant, including the versions of your:

Optionally any of the other dependencies involved

Ideally, creating a pull request with a (failing) test case demonstrating what’s wrong. This makes it easy for us to reproduce and fix the problem.

If you’re ready to take the plunge and contribute back some code or documentation please consider the following:

Search existing issues and PRs to see if there are already any similar proposals.

For substantial changes, we recommend raising a question first so that we can offer any advice or pointers based on previous experience.

The process should look like:

Fork the project on GitHub into your own account.

Clone your copy of django-import-export.

Make a new branch in git & commit your changes there.

Push your new branch up to GitHub.

Again, ensure there isn’t already an issue or pull request out there on it.

If there is and you feel you have a better fix, please take note of the issue number and mention it in your pull request.

Create a new pull request (based on your branch), including what the problem/feature is, versions of your software and referencing any related issues/pull requests.

We recommend setting up your editor to automatically indicate non-conforming styles (see Development).

In order to be merged into django-import-export, contributions must have the following:

works across all supported versions of Python/Django.

follows the existing style of the code base (mostly PEP-8).

comments included as needed to explain why the code functions as it does

A test case that demonstrates the previous flaw that now passes with the included patch.

If it adds/changes a public API, it must also include documentation for those changes.

Must be appropriately licensed (see Philosophy).

Adds yourself to the AUTHORS file.

If your contribution lacks any of these things, they will have to be added by a core contributor before being merged into django-import-export proper, which may take substantial time for the all-volunteer team to get to.

All files should be formatted using the black auto-formatter. This will be run by pre-commit if configured.

The project repository includes an .editorconfig file. We recommend using a text editor with EditorConfig support to avoid indentation and whitespace issues.

We allow up to 88 characters as this is the line length used by black. This check is included when you run flake8. Documentation, comments, and docstrings should be wrapped at 79 characters, even though PEP 8 suggests 72.

To install pre-commit:

If using git blame, you can ignore commits which made large changes to the code base, such as reformatting. Run this command from the base project directory:

Once you have cloned and checked out the repository, you can install a new development environment as follows:

You can run the test suite with:

To build a local version of the documentation:

The documentation will be present in docs/_build/html/index.html.

When generating or updating translation files with makemessages, use the make messages command. This command adds the –add-location=file arg to include only the source file path, not line numbers.

This keeps .po files cleaner and avoids unnecessary version control churn when line numbers shift due to unrelated code changes.

Translators can still trace strings back to their source using the file references.

---

## Advanced usage — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/advanced_usage.html

**Contents:**
- Advanced usage
- Customize resource options
  - Declare fields
  - Field ordering
  - Model relations
  - Explicit field declaration
- Field widgets
  - Modify render() return type
  - Custom workflow based on import values
- Using modelresource_factory

By default ModelResource introspects model fields and creates Field attributes with an appropriate Widget for each field.

Fields are generated automatically by introspection on the declared model class. The field defines the relationship between the resource we are importing (for example, a csv row) and the instance we want to update. Typically, the row data will map onto a single model instance. The row data will be set onto model instance attributes (including instance relations) during the import process.

In a simple case, the name of the row headers will map exactly onto the names of the model attributes, and the import process will handle this mapping. In more complex cases, model attributes and row headers may differ, and we will need to declare explicitly declare this mapping. See Explicit field declaration for more information.

You can optionally use the fields declaration to affect which fields are handled during import / export.

To affect which model fields will be included in a resource, use the fields option to whitelist fields:

Or the exclude option to blacklist fields:

If both fields and exclude are declared, the fields declaration takes precedence, and exclude is ignored.

When importing or exporting, the ordering defined by fields is used, however an explicit order for importing or exporting fields can be set using the either the import_order or export_order options:

The precedence for the order of fields for import / export is defined as follows:

import_order or export_order (if defined)

The order derived from the underlying model instance.

Where import_order or export_order contains a subset of fields then the import_order and export_order fields will be processed first.

If no fields, import_order or export_order is defined then fields are created via introspection of the model class. The order of declared fields in the model instance is preserved, and any non-model fields are last in the ordering.

When defining ModelResource fields it is possible to follow model relationships:

This example declares that the Author.name value (which has a foreign key relation to Book) will appear in the export.

Declaring the relationship using this syntax means the following:

The field will be skipped when importing data. To understand how to import model relations, see Importing model relations.

The default string value of the field will be exported. To have full control over the format of the export, see Explicit field declaration.

We can declare fields explicitly to give us more control over the relationship between the row and the model attribute. In the example below, we use the attribute kwarg to define the model attribute, and column_name to define the column name (i.e. row header):

The attribute parameter is optional, and if omitted it means that:

The field will be ignored during import.

The field will be present during export, but will have an empty value unless a dehydrate method is defined.

If using the fields attribute to declare fields then the declared resource attribute name must appear in the fields list:

Available field types and options.

A widget is an object associated with each field declaration. The widget has two roles:

Transform the raw import data into a python object which is associated with the instance (see clean()).

Export persisted data into a suitable export format (see render()).

There are widgets associated with character data, numeric values, dates, foreign keys. You can also define your own widget and associate it with the field.

A ModelResource creates fields with a default widget for a given field type via introspection. If the widget should be initialized with different arguments, this can be done via an explicit declaration or via the widgets dict.

For example, the published field is overridden to use a different date format. This format will be used both for importing and exporting resource:

Alternatively, widget parameters can be overridden using the widgets dict declaration:

Declaring fields may affect the export order of the fields. If this is an issue, you can declare the export_order attribute. See Field ordering.

By default, render() will return a string type for export. There may be use cases where a native type is required from export. If so, you can use the coerce_to_string parameter if the widget supports it.

By default, coerce_to_string is True, but if you set this to False, then the native type will be returned during export:

If exporting via the Admin interface, the export logic will detect if exporting to either XLSX, XLS or ODS format, and will set native types for Numeric, Boolean and Date values. This means that the coerce_to_string value will be ignored and the native types will be returned. This is because in most use-cases the native type will be expected in the exported format. If you need to modify this behavior and enforce string types in “binary” file formats then the only way to do this is to override the widget render() method.

Available widget types and options.

You can extend the import process to add workflow based on changes to persisted model instances.

For example, suppose you are importing a list of books and you require additional workflow on the date of publication. In this example, we assume there is an existing unpublished book instance which has a null ‘published’ field.

There will be a one-off operation to take place on the date of publication, which will be identified by the presence of the ‘published’ field in the import file.

To achieve this, we need to test the existing value taken from the persisted instance (i.e. prior to import changes) against the incoming value on the updated instance. Both instance and original are attributes of RowResult.

You can override the after_import_row() method to check if the value changes:

The original attribute will be null if skip_diff is True.

The instance attribute will be null if store_instance is False.

The modelresource_factory() function dynamically creates ModelResource classes for you. This is useful for creating resources without writing custom classes.

Create a simple resource for export:

Import data with custom configuration:

You can add custom fields and dehydrate methods:

The import process will include basic validation during import. This validation can be customized or extended if required.

The import process distinguishes between:

Validation errors which arise when failing to parse import data correctly.

General exceptions which arise during processing.

Errors are retained as Error instances in each RowResult instance, which is stored in the single Result instance which is returned from the import process.

The import_data() method takes optional parameters which can be used to customize the handling of errors. Refer to the method documentation for specific details.

During import of a row, each field is iterated and any ValueError errors raised by Widgets are stored in an instance of Django’s ValidationError.

Validation errors are retained within the invalid_rows list as a InvalidRow instance.

If importing programmatically, you can set the raise_errors parameter of import_data() to True, which will mean the process will exit at the first row which has errors:

The above process will exit with a row number and error (formatted for clarity):

To iterate over all validation errors produced from an import, pass False to raise_errors:

If using the Admin UI, errors are presented to the user during import (see below).

Generic errors are raised during import for cases which are not validation errors. For example, generic errors are usually raised at the point the model instance is saved, such as attempt to save a float to a int field. Because generic errors are raised from a lower point in the stack, it is not always possible to identify which field caused the error.

Generic errors are retained within the error_rows list as a ErrorRow instance.

The raise_errors parameter can be used during programmatic import to halt the import at the first error:

The above process will exit with a row number and error (formatted for clarity):

To iterate over all generic errors produced from an import, pass False to raise_errors:

full_clean() is only called on the model instance if the Resource option clean_model_instances is enabled.

Validation of input can be performed during import by a widget’s clean() method by raising a ValueError. Consult the widget documentation for more information.

You can supply your own field level validation by overriding clean(), for example:

Field level errors will be presented in the Admin UI, for example:

A screenshot showing a field specific error.

You can optionally configure import-export to perform model instance validation during import by enabling the clean_model_instances attribute.

You can override the full_clean() method to provide extra validation, either at field or instance level:

A screenshot showing a non field specific error.

You are free to subclass or replace the classes defined in results. Override any or all of the following hooks to customize error handling:

get_row_result_class()

get_error_result_class()

If you are importing data for a model instance which has a foreign key relationship to another model then import-export can handle the lookup and linking to the related model.

ForeignKeyWidget allows you to declare a reference to a related model. For example, if we are importing a ‘book’ csv file, then we can have a single field which references an author by name.

We would have to declare our BookResource to use the author name as the foreign key reference:

By default, ForeignKeyWidget will use ‘pk’ as the lookup field, hence we have to pass ‘name’ as the lookup field. This relies on ‘name’ being a unique identifier for the related model instance, meaning that a lookup on the related table using the field value will return exactly one result.

This is implemented as a Model.objects.get() query, so if the instance in not uniquely identifiable based on the given arg, then the import process will raise either DoesNotExist or MultipleObjectsReturned errors.

See also Creating non-existent relations.

Refer to the ForeignKeyWidget documentation for more detailed information. If importing large datasets, see the notes in ForeignKeyWidget performance considerations and consider using CachedForeignKeyWidget

If you are exporting a field which uses ForeignKeyWidget then the default formatting for the field will be applied. If you need better control over the format of the exported value (for example, formatting a date), then use a dehydrate method or create a subclass of ForeignKeyWidget. Override render() to create custom formatting of output.

ManyToManyWidget allows you to import m2m references. For example, we can import associated categories with our book import. The categories refer to existing data in a Category table, and are uniquely referenced by category name. We use the pipe separator in the import file, which means we have to declare this in the ManyToManyWidget declaration.

The examples above rely on the relation data being present prior to the import. It is a common use-case to create the data if it does not already exist. A simple way to achieve this is to override the ForeignKeyWidget clean() method:

Now you will need to declare the widget in the Resource:

The code above can be adapted to handle m2m relationships, see this thread.

The ForeignKeyWidget and ManyToManyWidget widgets will look for relations by searching the entire relation table for the imported value. This is implemented in the get_queryset() method. For example, for an Author relation, the lookup calls Author.objects.all().

In some cases, you may want to customize this behaviour, and it can be a requirement to pass dynamic values in. For example, suppose we want to look up authors associated with a certain publisher id. We can achieve this by passing the publisher id into the Resource constructor, which can then be passed to the widget:

The corresponding ForeignKeyWidget subclass:

Then if the import was being called from another module, we would pass the publisher_id into the Resource:

If you need to pass dynamic values to the Resource when importing via the Admin UI, refer to See How to dynamically set resource values.

The ForeignKeyWidget also supports using Django’s natural key functions. A manager class with the get_by_natural_key function is required for importing foreign key relationships by the field model’s natural key, and the model must have a natural_key function that can be serialized as a JSON list in order to export data.

The primary utility for natural key functionality is to enable exporting data that can be imported into other Django environments with different numerical primary key sequences. The natural key functionality enables handling more complex data than specifying either a single field or the PK.

The example below illustrates how to create a field on the BookResource that imports and exports its author relationships using the natural key functions on the Author model and modelmanager.

The resource _meta option use_natural_foreign_keys enables this setting for all Models that support it.

Read more at Django Serialization.

When you are importing a file using import-export, the file is processed row by row. For each row, the import process is going to test whether the row corresponds to an existing stored instance, or whether a new instance is to be created.

If an existing instance is found, then the instance is going to be updated with the values from the imported row, otherwise a new row will be created.

In order to test whether the instance already exists, import-export needs to use a field (or a combination of fields) in the row being imported. The idea is that the field (or fields) will uniquely identify a single instance of the model type you are importing.

To define which fields identify an instance, use the import_id_fields meta attribute. You can use this declaration to indicate which field (or fields) should be used to uniquely identify the row. If you don’t declare import_id_fields, then a default declaration is used, in which there is only one field: ‘id’.

For example, you can use the ‘isbn’ number instead of ‘id’ to uniquely identify a Book as follows:

If setting import_id_fields, you must ensure that the data can uniquely identify a single row. If the chosen field(s) select more than one row, then a MultipleObjectsReturned exception will be raised. If no row is identified, then DoesNotExist exception will be raised.

There are some use-cases where a field defined in import_id_fields is not present in the dataset. An example of this would be dynamic fields, where a field is generated from other data and then used as an identifier. For example:

In the above example, a dynamic field called hash_id is generated and added to the dataset. In this example, an error will be raised because hash_id is not present in the dataset. To resolve this, update the dataset before import to add the dynamic field as a header:

The instance pk and representation (i.e. output from repr()) can be accessed after import:

All ‘new’, ‘updated’ and ‘deleted’ instances can be accessed after import if the store_instance meta attribute is set.

For example, this snippet shows how you can retrieve persisted row data from a result:

If an existing instance is identified during import, then the existing instance will be updated, regardless of whether the data in the import row is the same as the persisted data or not. You can configure the import process to skip the row if it is duplicate by using setting skip_unchanged.

If skip_unchanged is enabled, then the import process will check each defined import field and perform a simple comparison with the existing instance, and if all comparisons are equal, then the row is skipped. Skipped rows are recorded in the row RowResult object.

You can override the skip_row() method to have full control over the skip row implementation.

Also, the report_skipped option controls whether skipped records appear in the import RowResult object, and whether skipped records will show in the import preview page in the Admin UI:

You may have a use-case where you need to set the same value on each instance created during import. For example, it might be that you need to set a value read at runtime on all instances during import.

You can define your resource to take the associated instance as a param, and then set it on each import instance:

See How to dynamically set resource values.

Import data often requires transformation or cleaning before it can be properly saved to your Django models. Import-export provides several hooks to manipulate data during the import process:

before_import() - Called before processing the entire dataset, allowing you to modify headers or perform dataset-level transformations.

before_import_row() - Called before processing each individual row, allowing you to transform or clean row data.

While the BooleanWidget is set up to accept common variations of “True” and “False” (and “None”), you may need to handle less common values or custom boolean representations.

The easiest way to transform custom boolean values is to override the before_import_row() method in your Resource class:

This approach allows you to handle domain-specific boolean values while keeping the import logic centralized and maintainable.

In the same way that it is possible to refer to the relationships of the model by defining a field with double underscore __ syntax, values within JSONObject/ JSONField can also be accessed but in this case it is necessary to specify it in attribute. If you will use the resource for import as well, you must mark the field as readonly. If you only want the field for export, marking it as readonly is not necessary:

In this case, the export looks like this:

Remember that the types that are annotated/stored within these fields are primitive JSON data types (strings, numbers, boolean, null) and also composite JSON data types (array and object). That is why, in the example, the birthday field within the author_json dictionary is displayed as a string. It is recommended that you always declare these fields as readonly even if you only want to use them for export.

Not all data can be easily extracted from an object/model attribute. In order to turn complicated data model into a (generally simpler) processed data structure on export, dehydrate_<fieldname> method should be defined:

In this case, the export looks like this:

It is also possible to pass a method name or a callable to the Field() constructor. If this method name or callable is supplied, then it will be called as the ‘dehydrate’ method. For example:

You can use filter_export() to filter querysets during export. See also Customize admin export forms.

The after_export() method allows you to modify the tablib dataset before it is rendered in the export format.

This can be useful for adding dynamic columns or applying custom logic to the final dataset.

If you would like to import one set of fields, and then export a different set, then the recommended way to do this is to define two resources:

If you are using these resources in the Admin UI, declare them in your admin class.

It is possible to modify the output of any XLSX export. The output bytes can be read and then modified using the openpyxl library (which can be included as an import_export dependency).

You can override get_export_data() as follows:

Customize the export file name by overriding get_export_filename().

To hook in the import-export workflow, you can connect to post_import, post_export signals:

There is specific consideration required if your application allows concurrent writes to data during imports.

For example, consider this scenario:

An import process is run to import new books identified by title.

The get_or_init_instance() is called and identifies that there is no existing book with this title, hence the import process will create it as a new record.

At that exact moment, another process inserts a book with the same title.

As the row import process completes, save() is called and an error is thrown because the book already exists in the database.

By default, import-export does not prevent this situation from occurring, therefore you need to consider what processes might be modifying shared tables during imports, and how you can mitigate risks. If your database enforces integrity, then you may get errors raised, if not then you may get duplicate data.

Potential solutions are:

Use one of the import workflow methods to lock a table during import if the database supports it.

This should only be done in exceptional cases because there will be a performance impact.

You will need to release the lock both in normal workflow and if there are errors.

Override do_instance_save() to perform a update_or_create(). This can ensure that data integrity is maintained if there is concurrent access.

Modify working practices so that there is no risk of concurrent writes. For example, you could schedule imports to only run at night.

This issue may be more prevalent if using bulk imports. This is because instances are held in memory for longer before being written in bulk, therefore there is potentially more risk of another process modifying an instance before it has been persisted.

Please refer to the API documentation for additional configuration options.

---

## Admin integration — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/admin_integration.html

**Contents:**
- Admin integration
- Importing
- Import confirmation
  - Customizable storage
  - How to format UI error messages
- Exporting
- Exporting via Admin action
  - Exporting large datasets
- Export from model instance change form
- Customize admin import forms

One of the main features of import-export is the support for integration with the Django Admin site. This provides a convenient interface for importing and exporting Django objects. Refer to the Django Admin documentation for details of how to enable and configure the admin site.

You can also install and run the example application to become familiar with Admin integration.

Integrating import-export with your application requires extra configuration.

Admin integration is achieved by subclassing ImportExportModelAdmin or one of the available mixins (ImportMixin, ExportMixin, ImportExportMixin):

Once this configuration is present (and server is restarted), ‘import’ and ‘export’ buttons will be presented to the user. Clicking each button will open a workflow where the user can select the type of import or export.

You can assign multiple resources to the resource_classes attribute. These resources will be presented in a select dropdown in the UI.

A screenshot of the change view with Import and Export buttons.

To enable import, subclass ImportExportModelAdmin or use one of the available mixins, i.e. ImportMixin, or ImportExportMixin.

Enabling import functionality means that a UI button will automatically be presented on the Admin page:

When clicked, the user will be directed into the import workflow. By default, import is a two step process, though it can be configured to be a single step process (see IMPORT_EXPORT_SKIP_ADMIN_CONFIRM).

The two step process is:

Select the file and format for import.

Preview the import data and confirm import.

A screenshot of the ‘import’ view.

A screenshot of the ‘confirm import’ view.

To support import confirmation, uploaded data is written to temporary storage after step 1 (choose file), and read back for final import after step 2 (import confirmation).

There are three mechanisms for temporary storage.

Temporary file storage on the host server (default). This is suitable for development only. Use of temporary filesystem storage is not recommended for production sites.

To modify which storage mechanism is used, please refer to the setting IMPORT_EXPORT_TMP_STORAGE_CLASS.

Your choice of temporary storage will be influenced by the following factors:

Sensitivity of the data being imported.

Volume and frequency of uploads.

Use of containers or load-balanced servers.

Temporary resources are removed when data is successfully imported after the confirmation step.

For sensitive data you will need to understand exactly how temporary files are being stored and to ensure that data is properly secured and managed.

If users do not complete the confirmation step of the workflow, or if there are errors during import, then temporary resources may not be deleted. This will need to be understood and managed in production settings. For example, using a cache expiration policy or cron job to clear stale resources.

If using MediaStorage as a storage module, then you can define which storage backend implementation is used to handle create / read / delete operations on the persisted data.

If using Django 4.2 or greater, use the STORAGES setting to define the backend, otherwise use IMPORT_EXPORT_DEFAULT_FILE_STORAGE.

You can either supply a path to your own custom storage backend, or use pre-existing backends such as django-storages.

If no custom storage implementation is supplied, then the Django default handler is used.

For example, if using django-storages, you can configure s3 as a temporary storage location with the following:

Admin UI import error messages can be formatted using the import_error_display attribute.

As with import, it is also possible to configure export functionality.

To do this, subclass ImportExportModelAdmin or use one of the available mixins, i.e. ExportMixin, or ImportExportMixin.

Enabling export functionality means that a UI button will automatically be presented on the Admin page:

When clicked, the user will be directed into the export workflow.

Export is a two step process. When the ‘export’ button is clicked, the user will be directed to a new screen, where ‘resource’, ‘fields’ and ‘file format’ can be selected.

The export ‘confirm’ page.

Once ‘submit’ is clicked, the export file will be automatically downloaded to the client (usually to the ‘Downloads’ folder).

It is possible to disable this extra step by setting the IMPORT_EXPORT_SKIP_ADMIN_EXPORT_UI flag, or by setting skip_export_form.

It’s possible to configure the Admin UI so that users can select which items they want to export:

To do this, simply declare an Admin instance which includes ExportActionMixin:

Then register this Admin:

Note that the above example refers specifically to the example application, you’ll have to modify this to refer to your own model instances. In the example application, the ‘Category’ model has this functionality.

When ‘Go’ is clicked for the selected items, the user will be directed to the export ‘confirm’ page.

It is possible to disable this extra step by setting the IMPORT_EXPORT_SKIP_ADMIN_ACTION_EXPORT_UI or IMPORT_EXPORT_SKIP_ADMIN_EXPORT_UI flags, or by setting skip_export_form_from_action or skip_export_form.

If deploying to a multi-tenant environment, you may need to ensure that one set of users cannot export data belonging to another set. To do this, filter the range of exportable items to be limited to only those items which users should be permitted to export. See get_export_queryset().

If exporting large datasets via the action menu, you may see Django’s SuspiciousOperation exception for ‘TooManyFieldsSent’. This is a built-in Django protection against Denial of Service attacks.

If you need to be able to export larger datasets via the action menu you can use the DATA_UPLOAD_MAX_NUMBER_FIELDS setting to increase or disable this check.

When export via admin action is enabled, then it is also possible to export from a model instance change form:

Export from model instance change form

When ‘Export’ is clicked, the user will be directed to the export ‘confirm’ page.

This button can be removed from the UI by setting the show_change_form_export attribute, for example:

It is possible to modify default import forms used in the model admin. For example, to add an additional field in the import form, subclass and extend the ImportForm (note that you may want to also consider ConfirmImportForm as importing is a two-step process).

To use your customized form(s), change the respective attributes on your ModelAdmin class:

For example, imagine you want to import books and set each book to have the same Author, selected from a dropdown. You can extend the import forms to include author field to select the author from.

Importing an E-Book using the example application demonstrates this.

A screenshot of a customized import view.

Customize forms (for example see tests/core/forms.py):

Customize ModelAdmin (for example see tests/core/admin.py):

In order to save the selected author along with the EBook, another couple of methods are required. Add the following to CustomBookAdmin class (in tests/core/admin.py):

Then add the following to EBookResource class (in tests/core/admin.py):

The selected author is now set as an attribute on the instance object. When the instance is saved, then the author is set as a foreign key relation to the instance.

To further customize the import forms, you might like to consider overriding the following ImportMixin methods:

get_import_form_class()

get_import_form_kwargs()

get_import_form_initial()

get_confirm_form_class()

get_confirm_form_kwargs()

The parameters can then be read from Resource methods, such as:

available mixins and options.

It is also possible to add fields to the export form so that export data can be filtered. For example, we can filter exports by Author.

A screenshot of a customized export view.

Customize forms (for example see tests/core/forms.py):

Customize ModelAdmin (for example see tests/core/admin.py):

Create a Resource subclass to apply the filter (for example see tests/core/admin.py):

In this example, we can filter an EBook export using the author’s name.

Create a custom form which defines ‘author’ as a required field.

Create a ‘CustomBookAdmin’ class which defines a Resource, and overrides get_export_resource_kwargs(). This ensures that the author id will be passed to the Resource constructor.

Create a Resource which is instantiated with the author_id, and can filter the queryset as required.

It is possible to set multiple resources both to import and export ModelAdmin classes. The ImportMixin, ExportMixin, ImportExportMixin and ImportExportModelAdmin classes accepts subscriptable type (list, tuple, …) as resource_classes parameter.

The subscriptable could also be returned from one of the following:

get_resource_classes()

get_import_resource_classes()

get_export_resource_classes()

If there are multiple resources, the resource chooser appears in import/export admin form. The displayed name of the resource can be changed through the name parameter of the Meta class.

Use multiple resources:

There are a few use cases where it is desirable to dynamically set values in the Resource. For example, suppose you are importing via the Admin console and want to use a value associated with the authenticated user in import queries.

Suppose the authenticated user (stored in the request object) has a property called publisher_id. During import, we want to filter any books associated only with that publisher.

First of all, override the get_import_resource_kwargs() method so that the request user is retained:

Now you can add a constructor to your Resource to store the user reference, then override get_queryset() to return books for the publisher:

import-export extends the Django Admin interface. There is a possibility that clashes may occur with other 3rd party libraries which also use the admin interface.

Issues have been raised due to conflicts with setting change_list_template. There is a workaround listed here. Also, refer to this issue. If you want to patch your own installation to fix this, a patch is available here.

If you use import-export using with django-debug-toolbar. then you need to configure debug_toolbar=False or DEBUG=False, It has been reported that the the import/export time will increase ~10 times.

Enabling the Admin interface means that you should consider the security implications. Some or all of the following points may be relevant.

What is the source of your import file?

Is this coming from an external source where the data could be untrusted?

Could source data potentially contain malicious content such as script directives or Excel formulae?

Even if data comes from a trusted source, is there any content such as HTML which could cause issues when rendered in a web page?

If there is malicious content in stored data, what is the risk of exporting this data?

Could untrusted input be executed within a spreadsheet?

Are spreadsheets sent to other parties who could inadvertently execute malicious content?

Could data be exported to other formats, such as CSV, TSV or ODS, and then opened using Excel?

Could any exported data be rendered in HTML? For example, csv is exported and then loaded into another web application. In this case, untrusted input could contain malicious code such as active script content.

You should in all cases review Django security documentation before deploying a live Admin interface instance.

Please read the following topics carefully to understand how you can improve the security of your implementation.

By default, import-export does not sanitize or process imported data. Malicious content, such as script directives, can be imported into the database, and can be exported without any modification.

HTML content, if exported into ‘html’ format, will be sanitized to remove scriptable content. This sanitization is performed by the tablib library.

You can optionally configure import-export to sanitize Excel formula data on export. See IMPORT_EXPORT_ESCAPE_FORMULAE_ON_EXPORT.

Enabling this setting only sanitizes data exported using the Admin Interface. If exporting data programmatically, then you will need to apply your own sanitization.

Limiting the available import or export format types can be considered. For example, if you never need to support import or export of spreadsheet data, you can remove this format from the application.

Imports and exports can be restricted using the following settings:

IMPORT_EXPORT_FORMATS

Consider setting permissions to define which users can import and export.

IMPORT_EXPORT_IMPORT_PERMISSION_CODE

IMPORT_EXPORT_EXPORT_PERMISSION_CODE

Refer to SECURITY.md for details on how to escalate security issues you may have found in import-export.

---
