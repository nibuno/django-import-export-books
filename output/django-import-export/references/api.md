# Django-Import-Export - Api

**Pages:** 10

---

## Admin — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/api_admin.html

**Contents:**
- Admin

For instructions on how to use the models and mixins in this module, please refer to Admin integration.

Mixin with export functionality implemented as an admin action.

template for change form

Action runs on POST from instance action menu (if enabled).

Adds the export action to the list of available actions.

Flag to indicate whether to show ‘export’ button on change form

Subclass of ModelAdmin with export functionality implemented as an admin action.

This is intended to be mixed with ModelAdmin.

Handles the default workflow for both the export form and the export of data to file.

Form class to use for the initial export step. Assign to ExportForm if you would like to disable selectable fields feature.

alias of SelectableFieldsExportForm

template for export view

Returns file_format representation for given queryset.

Get the form class used to read the export format.

Returns export queryset. The queryset is obtained by calling ModelAdmin get_queryset().

Default implementation respects applied search and filters.

Returns whether a request has export permission.

template for change_list view

Subclass of ExportActionModelAdmin with import/export functionality. Export functionality is implemented as an admin action.

Import and export mixin.

template for change_list view

Subclass of ModelAdmin with import/export functionality.

This is intended to be mixed with django.contrib.admin.ModelAdmin https://docs.djangoproject.com/en/dev/ref/contrib/admin/

form class to use for the confirm import step

alias of ConfirmImportForm

Added in version 3.0.

Return a form instance to use for the ‘confirm’ import step. This method can be extended to make dynamic form updates to the form after it has been instantiated. You might also look to override the following:

get_confirm_form_class()

get_confirm_form_kwargs()

get_confirm_form_initial()

Added in version 3.0.

Return a form instance to use for the ‘initial’ import step. This method can be extended to make dynamic form updates to the form after it has been instantiated. You might also look to override the following:

get_import_form_class()

get_import_form_kwargs()

get_import_form_initial()

get_import_resource_classes()

Added in version 3.0.

Return the form class to use for the ‘confirm’ import step. If you only have a single custom form class, you can set the confirm_form_class attribute to change this for your subclass.

Added in version 3.0.

Return a dictionary of initial field values to be provided to the ‘confirm’ form.

Added in version 3.0.

Return a dictionary of values with which to initialize the ‘confirm’ form (including the initial values returned by get_confirm_form_initial()).

Prepare kwargs for import_data.

Added in version 3.0.

Return the form class to use for the ‘import’ step. If you only have a single custom form class, you can set the import_form_class attribute to change this for your subclass.

Added in version 3.0.

Return a dictionary of initial field values to be provided to the ‘import’ form.

Added in version 3.0.

Return a dictionary of values with which to initialize the ‘import’ form (including the initial values returned by get_import_form_initial()).

Override this method to provide additional kwargs to temp storage class.

Returns whether a request has import permission.

Perform a dry_run of the import to make sure the import will not result in errors. If there are no errors, save the user uploaded file to a local temp file that will be used by ‘process_import’ for the actual import.

control which UI elements appear when import errors are displayed. Available options: ‘message’, ‘row’, ‘traceback’

template for change_list view

form class to use for the initial import step

template for import view

Perform the actual import action (after the user has confirmed the import)

---

## Forms — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/api_forms.html

**Contents:**
- Forms

---

## Instance loaders — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/api_instance_loaders.html

**Contents:**
- Instance loaders

Base abstract implementation of instance loader.

Instance loader for Django model.

Lookup for model instance by import_id_fields.

Loads all possible model instances in dataset avoid hitting database for every get_instance call.

This instance loader work only when there is one import_id_fields field.

---

## Exceptions — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/api_exceptions.html

**Contents:**
- Exceptions
- ImportExportError
- FieldError
- ImportError

A generic exception for all others to extend.

Raised when a field encounters an error.

A wrapper for errors thrown from the import process.

error – The underlying error that occurred.

number – The row number of the row containing the error (if obtainable).

row – The row containing the error (if obtainable).

---

## Temporary storages — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/api_tmp_storages.html

**Contents:**
- Temporary storages
- TempFolderStorage
- CacheStorage
- MediaStorage

By default memcache maximum size per key is 1MB, be careful with large files.

---

## Resources — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/api_resources.html

**Contents:**
- Resources
- Resource
- ModelResource
- ResourceOptions (Meta)
- modelresource_factory

Resource defines how objects are mapped to their import and export representations and handle importing and exporting data.

An optional dict of kwargs. Subclasses can use kwargs to pass dynamic values to enhance import / exports.

Override to add additional logic. Does nothing by default.

instance – A new or existing model instance.

row – A dict containing key / value data for the row to be imported.

**kwargs – See import_row()

Override to add additional logic. Does nothing by default.

queryset – The queryset for export.

dataset – A tablib.Dataset.

**kwargs – Metadata which may be associated with the export.

Override to add additional logic. Does nothing by default.

dataset – A tablib.Dataset.

result – A import_export.results.Result implementation containing a summary of the import.

**kwargs – See import_row()

Override to add additional logic. Does nothing by default.

row – A dict containing key / value data for the row to be imported.

row_result – A RowResult instance. References the persisted instance as an attribute.

**kwargs – See import_row()

Override to add additional logic. Does nothing by default.

instance – A new or existing model instance.

new – a boolean flag indicating whether instance is new or existing.

row – A dict containing key / value data for the row to be imported.

**kwargs – See import_row()

Override to add additional logic. Does nothing by default.

instance – A new or existing model instance.

row – A dict containing key / value data for the row to be imported.

**kwargs – See import_row()

Override to add additional logic. Does nothing by default.

instance – A new or existing model instance.

row – A dict containing key / value data for the row to be imported.

**kwargs – See import_row()

Override to add additional logic. Does nothing by default.

queryset – The queryset for export.

**kwargs – Metadata which may be associated with the export.

Override to add additional logic. Does nothing by default.

dataset – A tablib.Dataset.

**kwargs – See import_row()

Override to add additional logic. Does nothing by default.

row – A dict containing key / value data for the row to be imported.

**kwargs – See import_row()

Override to add additional logic. Does nothing by default.

instance – A new or existing model instance.

row – A dict containing key / value data for the row to be imported.

**kwargs – See import_row()

Creates objects by calling bulk_create.

Deletes objects by filtering on a list of instances to be deleted, then calling delete() on the entire queryset.

Updates objects by calling bulk_update.

Calls instance.delete() as long as dry_run is not set. If use_bulk then instances are appended to a list for bulk import.

instance – A new or existing model instance.

row – A dict containing key / value data for the row to be imported.

**kwargs – See import_row()

A method specifically to provide a single overridable hook for the instance save operation. For example, this can be overridden to implement update_or_create().

instance – The model instance to be saved.

is_create – A boolean flag to indicate whether this is a new object to be created, or an existing object to be updated.

queryset – The queryset for export (optional).

Override to filter an export queryset.

queryset – The queryset for export.

**kwargs – Metadata which may be associated with the export.

The filtered queryset.

Returns True if row importing should delete instance.

Default implementation returns False. Override this method to handle deletion.

row – A dict containing key / value data for the row to be imported.

instance – A new or existing model instance.

Returns the fields to be included in calls to bulk_update(). import_id_fields are removed because id fields cannot be supplied to bulk_update().

Returns the class used to display the diff for an imported instance.

Diff representation headers.

Returns the class used to store an error resulting from an import.

Returns the field name for a given field.

Calls the InstanceLoader.

Either fetches an already existing instance or initializes a new one.

Returns the class used to store the result of an import.

Returns the class used to store the result of a row import.

Get fields visible to users in export interface

Get fields visible to users in admin interface.

Deprecated since version 5: Use get_user_visible_import_fields() or get_user_visible_export_fields() instead for explicit context-aware field selection. This method will be removed in version 6.0.

Get fields visible to users in import interface

Imports data from tablib.Dataset. Refer to Import workflow for a more complete description of the whole import process.

dataset – A tablib.Dataset.

raise_errors – Whether errors should be printed to the end user or raised regularly.

use_transactions – If True the import process will be processed inside a transaction.

collect_failed_rows – If True the import process will create a new dataset object comprising failed rows and errors. This can be useful for debugging purposes but will cause higher memory usage for larger datasets. See failed_dataset.

rollback_on_validation_errors – If both use_transactions and rollback_on_validation_errors are set to True, the import process will be rolled back in case of ValidationError.

dry_run – If dry_run is set, or an error occurs, if a transaction is being used, it will be rolled back.

**kwargs – Metadata which may be associated with the import.

Handles persistence of the field data.

field – A import_export.fields.Field instance.

instance – A new or existing model instance.

row – A dict containing key / value data for the row to be imported.

is_m2m – A boolean value indicating whether or not this is a many-to-many field.

**kwargs – See import_row()

Traverses every field in this Resource and calls import_field(). If import_field() results in a ValueError being raised for one of more fields, those errors are captured and reraised as a single, multi-field ValidationError.

instance – A new or existing model instance.

row – A dict containing key / value data for the row to be imported.

**kwargs – See import_row()

Imports data from tablib.Dataset. Refer to Import workflow for a more complete description of the whole import process.

row – A dict of the ‘row’ to import. A row is a dict of data fields so can be a csv line, a JSON object, a YAML object etc.

instance_loader – The instance loader to be used to load the model instance associated with the row (if there is one).

**kwargs – See below.

dry_run (boolean) – A True value means that no data should be persisted.

use_transactions (boolean) – A True value means that transactions will be rolled back.

row_number (int) – The index of the row being imported.

Initializes an object. Implemented in import_export.resources.ModelResource.init_instance().

Takes care of saving the object to the database.

Objects can be created in bulk if use_bulk is enabled.

instance – The instance of the object to be persisted.

is_create – A boolean flag to indicate whether this is a new object to be created, or an existing object to be updated.

row – A dict representing the import row.

**kwargs – See :meth:`import_row

Model instance need to have a primary key value before a many-to-many relationship can be used.

instance – A new or existing model instance.

row – A dict containing key / value data for the row to be imported.

**kwargs – See import_row()

Returns True if row importing should be skipped.

Default implementation returns False unless skip_unchanged == True and skip_diff == False.

If skip_diff is True, then no comparisons can be made because original will be None.

When left unspecified, skip_diff and skip_unchanged both default to False, and rows are never skipped.

By default, rows are not skipped if validation errors have been detected during import. You can change this behavior and choose to ignore validation errors by overriding this method.

Override this method to handle skipping rows meeting certain conditions.

Use super if you want to preserve default handling while overriding

instance – A new or updated model instance.

original – The original persisted model instance.

row – A dict containing key / value data for the row to be imported.

import_validation_errors – A dict containing key / value data for any identified validation errors.

Takes any validation errors that were raised by import_instance(), and combines them with validation errors raised by the instance’s full_clean() method. The combined errors are then re-raised as single, multi-field ValidationError.

If the clean_model_instances option is False, the instances’s full_clean() method is not called, and only the errors raised by import_instance() are re-raised.

ModelResource is Resource subclass for handling Django models.

An optional dict of kwargs. Subclasses can use kwargs to pass dynamic values to enhance import / exports.

Reset the SQL sequences after new objects are imported

Returns a Resource Field instance for the given Django model field.

Prepare widget for fk and o2o fields

Prepare widget for m2m field

Returns a queryset of all objects for this model. Override this if you want to limit the returned queryset.

Initializes a new Django model.

Returns the widget that would likely be associated with each Django type.

Includes mapping of Postgres Array field. In the case that psycopg2 is not installed, we consume the error and process the field regardless.

Returns widget kwargs for given field_name.

The inner Meta class allows for class-level configuration of how the Resource should behave. The following options are available:

The batch_size parameter controls how many objects are created in a single query. The default is to create objects in batches of 1000. See bulk_create(). This parameter is only used if use_bulk is True.

Controls the chunk_size argument of Queryset.iterator or, if prefetch_related is used, the per_page attribute of Paginator.

Controls whether full_clean is called during the import process to identify potential validation errors for each (non skipped) row. The default value is False.

Controls what introspected fields the Resource should NOT include. A blacklist of fields.

Controls export order for columns.

Controls what introspected fields the Resource should include. A whitelist of fields.

If True, this parameter will prevent imports from checking the database for existing instances. Enabling this parameter is a performance enhancement if your import dataset is guaranteed to contain new instances.

Controls which object fields will be used to identify existing instances.

Controls import order for columns.

Controls which class instance will take care of loading existing objects.

Django Model class or full application label string. It is used to introspect available fields.

Controls if the result reports skipped rows. Default value is True.

Controls whether or not an instance should be diffed following import.

By default, an instance is copied prior to insert, update or delete. After each row is processed, the instance’s copy is diffed against the original, and the value stored in each RowResult. If diffing is not required, then disabling the diff operation by setting this value to True improves performance, because the copy and comparison operations are skipped for each row.

If enabled, then skip_row() checks do not execute, because ‘skip’ logic requires comparison between the stored and imported versions of a row.

If enabled, then HTML row reports are also not generated, meaning that the skip_html_diff value is ignored.

The default value is False.

Controls whether or not a HTML report is generated after each row. By default, the difference between a stored copy and an imported instance is generated in HTML form and stored in each RowResult.

The HTML report is used to present changes in the import confirmation page in the admin site, hence when this value is True, then changes will not be presented on the confirmation screen.

If the HTML report is not required, then setting this value to True improves performance, because the HTML generation is skipped for each row. This is a useful optimization when importing large datasets.

The default value is False.

Controls if the import should skip unchanged records. If True, then each existing instance is compared with the instance to be imported, and if there are no changes detected, the row is recorded as skipped, and no database update takes place.

The advantages of enabling this option are:

Avoids unnecessary database operations which can result in performance improvements for large datasets.

Skipped records are recorded in each RowResult.

Skipped records are clearly visible in the import confirmation page.

For the default skip_unchanged logic to work, the skip_diff must also be False (which is the default):

Default value is False.

If True, the row instance will be stored in each RowResult. Enabling this parameter will increase the memory usage during import which should be considered when importing large datasets.

This value will always be set to True when importing via the Admin UI. This is so that appropriate LogEntry instances can be created.

If True, each row’s raw data will be stored in each RowResult. Enabling this parameter will increase the memory usage during import which should be considered when importing large datasets.

Controls whether import operations should be performed in bulk. By default, an object’s save() method is called for each row in a data set. When bulk is enabled, objects are saved using bulk operations.

If True, this value will be passed to all foreign key widget fields whose models support natural foreign keys. That is, the model has a natural_key function and the manager has a get_by_natural_key() function.

Controls if import should use database transactions. Default value is None meaning settings.IMPORT_EXPORT_USE_TRANSACTIONS will be evaluated.

DB Connection name to use for db transactions. If not provided, router.db_for_write(model) will be evaluated and if it’s missing, DEFAULT_DB_ALIAS constant (“default”) is used.

This dictionary defines widget kwargs for fields.

Factory for creating ModelResource class for given Django model. This factory function creates a ModelResource class dynamically, with support for custom fields, methods.

model – Django model class

resource_class – Base resource class (default: ModelResource)

meta_options – Meta options dictionary

custom_fields – Dictionary mapping field names to Field object

dehydrate_methods – Dictionary mapping field names to dehydrate method (Callable)

---

## Fields — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/api_fields.html

**Contents:**
- Fields

Field represents a mapping between an instance field and a representation of the field’s data.

attribute – A string of either an instance attribute or callable of the instance.

column_name – An optional column name for the column that represents this field in the export.

widget – Defines a widget that will be used to represent this field’s data in the export, or transform the value during import.

readonly – A Boolean which defines if this field will be ignored during import.

default – This value will be returned by clean() if this field’s widget returned a value defined in empty_values.

saves_null_values – Controls whether null values are saved on the instance. This can be used if the widget returns null, but there is a default instance value which should not be overwritten.

dehydrate_method – You can provide a dehydrate_method as a string to use instead of the default dehydrate_{field_name} syntax, or you can provide a callable that will be executed with the instance as its argument.

m2m_add – changes save of this field to add the values, if they do not exist, to a ManyToMany field instead of setting all values. Only useful if field is a ManyToMany field.

Translates the value stored in the imported datasource to an appropriate Python object and returns it.

Returns value from the provided instance converted to export representation.

Returns method name to be used for dehydration of the field. Defaults to dehydrate_{field_name}

Returns the value of the instance’s attribute.

If this field is not declared readonly, the instance’s attribute will be set to the value returned by clean().

---

## Widgets — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/api_widgets.html

**Contents:**
- Widgets

A Widget handles converting between import and export representations.

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

Returns an appropriate python object for an imported value. For example, a date string will be converted to a python datetime instance.

value – The value to be converted to a native type.

row – A dict containing row key/value pairs.

**kwargs – Optional kwargs.

Returns an export representation of a python value.

value – The python value to be rendered.

obj – The model instance from which the value is taken. This parameter is deprecated and will be removed in a future release.

By default, this value will be a string, with None values returned as empty strings.

Widget for converting numeric fields.

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

Returns an export representation of a python value.

value – The python value to be rendered.

obj – The model instance from which the value is taken. This parameter is deprecated and will be removed in a future release.

By default, this value will be a string, with None values returned as empty strings.

Widget for converting integer fields.

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

Converts the input value to a Python integer.

Uses Decimal for precise conversion to handle locale-specific number formatting.

value – The value to be converted to integer. Can be a string or numeric type.

row – The current row being processed.

**kwargs – Optional keyword arguments.

Optional keyword arguments.

A Python int instance, or None if value is empty.

ValueError – If the value cannot be converted to integer.

InvalidOperation – If Decimal conversion fails.

Widget for converting decimal fields.

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

Converts the input value to a Python Decimal for precise numeric operations.

value – The value to be converted to Decimal. Can be a string or numeric type.

row – The current row being processed.

**kwargs – Optional keyword arguments.

Optional keyword arguments.

A Python Decimal instance, or None if value is empty.

InvalidOperation – If the value cannot be converted to Decimal.

Widget for converting text fields.

allow_blank – If True, then clean() will return null values as empty strings, otherwise as None.

Converts the input value to a string, handling None values based on allow_blank setting.

value – The value to be converted to string.

row – The current row being processed.

**kwargs – Optional keyword arguments.

Optional keyword arguments.

A string representation of the value. Returns empty string if value is None and allow_blank is True, otherwise returns None.

Returns an export representation of a python value.

value – The python value to be rendered.

obj – The model instance from which the value is taken. This parameter is deprecated and will be removed in a future release.

By default, this value will be a string, with None values returned as empty strings.

Widget for converting boolean fields.

The widget assumes that True, False, and None are all valid values, as to match Django’s BooleanField. That said, whether the database/Django will actually accept NULL values will depend on if you have set null=True on that Django field.

Recognizes standard boolean representations. For custom boolean values, see Custom Boolean value handling in the advanced usage documentation.

Converts the input value to a Python boolean or None.

Recognizes common string representations of boolean values: - True values: ‘1’, 1, True, ‘true’, ‘TRUE’, ‘True’ - False values: ‘0’, 0, False, ‘false’, ‘FALSE’, ‘False’ - Null values: ‘’, None, ‘null’, ‘NULL’, ‘none’, ‘NONE’, ‘None’

value – The value to be converted to boolean.

row – The current row being processed.

**kwargs – Optional keyword arguments.

Optional keyword arguments.

True, False, or None depending on the input value.

True is represented as 1, False as 0, and None/NULL as an empty string. If coerce_to_string is False, the python Boolean type is returned (may be None).

True is represented as 1, False as 0, and None/NULL as an empty string.

If coerce_to_string is False, the python Boolean type is returned (may be None).

Widget for converting date fields to Python date instances.

Takes optional format parameter. If none is set, either settings.DATE_INPUT_FORMATS or "%Y-%m-%d" is used.

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

Converts a date string to a Python date instance using configured formats.

Attempts to parse the value using formats specified during widget initialization. If no format was provided, uses settings.DATE_INPUT_FORMATS or “%Y-%m-%d”.

value – A date string to be parsed, or an existing date instance.

row – The current row being processed.

**kwargs – Optional keyword arguments.

Optional keyword arguments.

A Python date instance, or None if value is empty.

ValueError – If the value cannot be parsed using any of the defined formats.

Returns an export representation of a python value.

value – The python value to be rendered.

obj – The model instance from which the value is taken. This parameter is deprecated and will be removed in a future release.

By default, this value will be a string, with None values returned as empty strings.

Widget for converting time fields.

Takes optional format parameter. If none is set, either settings.DATETIME_INPUT_FORMATS or "%H:%M:%S" is used.

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

A python time instance.

ValueError if the value cannot be parsed using defined formats.

Returns an export representation of a python value.

value – The python value to be rendered.

obj – The model instance from which the value is taken. This parameter is deprecated and will be removed in a future release.

By default, this value will be a string, with None values returned as empty strings.

Widget for converting datetime fields to Python datetime instances.

Takes optional format parameter. If none is set, either settings.DATETIME_INPUT_FORMATS or "%Y-%m-%d %H:%M:%S" is used.

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

A python datetime instance.

ValueError if the value cannot be parsed using defined formats.

Returns an export representation of a python value.

value – The python value to be rendered.

obj – The model instance from which the value is taken. This parameter is deprecated and will be removed in a future release.

By default, this value will be a string, with None values returned as empty strings.

Widget for converting time duration fields.

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

A python duration instance.

ValueError if the value cannot be parsed.

Returns an export representation of a python value.

value – The python value to be rendered.

obj – The model instance from which the value is taken. This parameter is deprecated and will be removed in a future release.

By default, this value will be a string, with None values returned as empty strings.

Widget for an Array field. Can be used for Postgres’ Array field.

separator – Defaults to ','

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

Converts a separated string into a Python array.

Splits the input string by the configured separator. Empty strings result in empty arrays rather than arrays containing empty strings.

value – A string containing values separated by the configured separator.

row – The current row being processed.

**kwargs – Optional keyword arguments.

Optional keyword arguments.

A Python list derived from splitting the value by separator. Returns an empty list if value is None or empty.

A string with values separated by separator. If coerce_to_string is False, the native array will be returned. If value is None, None will be returned if coerce_to_string is False, otherwise an empty string will be returned.

A string with values separated by separator. If coerce_to_string is False, the native array will be returned. If value is None, None will be returned if coerce_to_string

is False, otherwise an empty string will be returned.

Widget for a JSON object (especially required for jsonb fields in PostgreSQL database.)

value – Defaults to JSON format.

The widget covers two cases: Proper JSON string with double quotes, else it tries to use single quotes and then convert it to proper JSON.

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

Parses the input value as JSON and returns the corresponding Python object.

Attempts to parse as valid JSON first, then falls back to single-quote format by converting single quotes to double quotes before parsing.

value – A JSON string to be parsed.

row – The current row being processed.

**kwargs – Optional keyword arguments.

Optional keyword arguments.

The parsed Python object (dict, list, etc.) or None if value is empty.

JSONDecodeError – If the value cannot be parsed as JSON.

A JSON formatted string derived from value. coerce_to_string has no effect on the return value.

Widget for a ForeignKey field which looks up a related model using either the PK or a user specified field that uniquely identifies the instance in both export and import.

The lookup field defaults to using the primary key (pk) as lookup criterion but can be customized to use any field on the related model.

Unlike specifying a related field in your resource like so…

…using a ForeignKeyWidget has the advantage that it can not only be used for exporting, but also importing data with foreign key relationships.

Here’s an example on how to use ForeignKeyWidget to lookup related objects using Author.name instead of Author.pk:

model – The Model the ForeignKey refers to (required).

field – A field on the related model used for looking up a particular object.

use_natural_foreign_keys – Use natural key functions to identify related object, default to False

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

a single Foreign Key instance derived from the args. None can be returned if the value passed is a null value.

value – The field’s value in the dataset.

row – The dataset’s current row.

**kwargs – Optional kwargs.

ObjectDoesNotExist if no valid instance can be found.

the key value pairs used to identify a model instance. Override this to customize instance lookup.

value – The field’s value in the dataset.

row – The dataset’s current row.

**kwargs – Optional kwargs.

Returns a queryset of all objects for this Model.

Overwrite this method if you want to limit the pool of objects from which the related object is retrieved.

value – The field’s value in the dataset.

row – The dataset’s current row.

*args – Optional args.

**kwargs – Optional kwargs.

As an example; if you’d like to have ForeignKeyWidget look up a Person by their pre- and lastname column, you could subclass the widget like so:

A string representation of the related value. If use_natural_foreign_keys, the value’s natural key is returned. coerce_to_string has no effect on the return value.

A ForeignKeyWidget subclass that caches the queryset results to minimize database hits during import. The default ForeignKeyWidget makes query for each row, which can be inefficient for large imports. This widget fetches all related instances once and caches them in memory for subsequent lookups.

Using this class has some limitations:

It does not support caching when use_natural_foreign_keys=True is set.

It calls get_queryset() only once, so if the queryset depends on the row data, this widget may not work as expected. You must be sure that the queryset is static for all rows. Avoid using CachedForeignKeyWidget in the following way:

It makes more sense to filter by static values:

It stores data in a hash table where the key is a tuple of the fields that returned by get_lookup_kwargs(). You must be sure that the lookup fields are the same for all rows. If the lookup fields differ between rows, this widget may not work as expected. The following example is incorrect usage:

It performs lookup on Python side, so the filtering logic with non-text data types may not work:

It does not support complex lookups like __gt, __lt, or filtering over relationships in the get_lookup_kwargs(). For example, the following code won’t work:

model – The Model the ForeignKey refers to (required).

field – A field on the related model used for looking up a particular object.

use_natural_foreign_keys – Use natural key functions to identify related object, default to False

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

Widget that converts between representations of a ManyToMany relationships as a list and an actual ManyToMany field.

model – The model the ManyToMany field refers to (required).

separator – Defaults to ','.

field – A field on the related model. Default is pk.

coerce_to_string – If True, render() will return a string representation of the value, otherwise the value is returned.

Converts a separated string of values into a QuerySet for ManyToMany relationships.

Splits the input by the configured separator and looks up model instances using the specified field. Filters out empty values after splitting.

value – String of separated values, or a single numeric value.

row – The current row being processed.

**kwargs – Optional keyword arguments.

Optional keyword arguments.

A QuerySet containing the related model instances, or an empty QuerySet if no value provided.

A string with values separated by separator. None values are returned as empty strings. coerce_to_string has no effect on the return value.

---

## Mixins — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/api_mixins.html

**Contents:**
- Mixins
- BaseImportExportMixin
- BaseImportMixin
- BaseExportMixin
- ExportViewMixin
- ExportViewFormMixin

Base mixin for functionality related to importing and exporting via the Admin interface.

Return subscriptable type (list, tuple, …) containing resource classes :param request: The request object. :returns: The Resource classes.

Return the index of the resource class defined in the form.

form – The form object.

The index of the resource as an int.

Return the kwargs which are to be passed to the Resource constructor. Can be overridden to provide additional kwarg params.

request – The request object.

kwargs – Keyword arguments.

The Resource kwargs (by default, is the kwargs passed).

Identify which class should be used for import :param form: The form object. :param request: The request object. :returns: The import Resource class.

Returns available import formats.

request – The request object.

Returns ResourceClass subscriptable (list, tuple, …) to use for import.

Returns kwargs which will be passed to the Resource constructor. :param request: The request object. :param kwargs: Keyword arguments. :returns: The kwargs (dict)

If enabled, the import workflow skips the import confirm page and imports the data directly. See IMPORT_EXPORT_SKIP_ADMIN_CONFIRM.

Identify which class should be used for export :param request: The request object. :param form: The form object. :returns: The export Resource class.

Returns available export formats.

Returns ResourceClass subscriptable (list, tuple, …) to use for export. :param request: The request object. :returns: The Resource classes.

Returns kwargs which will be passed to the Resource constructor. :param request: The request object. :param kwargs: Keyword arguments. :returns: The kwargs (dict)

If enabled, the export workflow skips the export form and exports the data directly. See IMPORT_EXPORT_SKIP_ADMIN_EXPORT_UI.

If enabled, the export workflow from Admin UI action menu skips the export form and exports the data directly. See IMPORT_EXPORT_SKIP_ADMIN_ACTION_EXPORT_UI.

alias of SelectableFieldsExportForm

Returns file_format representation for given queryset.

Constructor. Called in the URLconf; can contain helpful extra keyword arguments, and other things.

If the form is valid, redirect to the supplied URL.

---

## Results — django-import-export 4.3.15.dev28 documentation

**URL:** https://django-import-export.readthedocs.io/en/latest/api_results.html

**Contents:**
- Results
- Result
- RowResult
- InvalidRow

The collection of rows which had generic errors.

A custom Dataset containing only failed rows and associated errors.

Returns a boolean indicating whether the import process resulted in any critical (non-validation) errors for this result.

Returns a boolean indicating whether the import process resulted in any validation errors for this result.

The collection of rows which had validation errors.

The rows associated with the result.

Container for values relating to a row import.

A HTML representation of the difference between the ‘original’ and ‘updated’ model instance.

An instance of Error which may have been raised during import.

A string identifier which identifies what type of import was performed.

A reference to the model instance which was created, updated or deleted.

True if import type is ‘delete’, otherwise False.

True if import type is ‘error’, otherwise False.

True if import type is ‘invalid’, otherwise False.

True if import type is ‘new’, otherwise False.

True if import type is ‘skip’, otherwise False.

True if import type is ‘update’, otherwise False.

True if import type is not ‘error’ or ‘invalid’, otherwise False.

The instance id (used in Admin UI)

The object representation (used in Admin UI)

A reference to the model instance before updates were applied. This value is only set for updates.

Retain the raw values associated with each imported row.

Contains any ValidationErrors which may have been raised during import.

A row that resulted in one or more ValidationError being raised during import.

Returns the total number of validation errors for this row.

Returns a dictionary of field-specific validation errors for this row.

Returns a list of non field-specific validation errors for this row.

---
