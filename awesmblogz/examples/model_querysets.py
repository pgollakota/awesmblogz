# This file contains various snippets to test various queryset methods.
# Try out various snippets at the command line and check the answers.


# Accessing the manager
# ---------------------

from awesmblogz.muzings.models import Entry
type(Entry)  # django.db.models.base.ModelBase
# objects attribute of Entry class returns its Manager
Entry.objects  # <django.db.models.manager.Manager at 0x...>


# Retrieving ALL Records
# ----------------------
all_entries = Entry.objects.all()
type(all_entries)  # django.db.models.query.QuerySet


# Examining the raw sql of a queryset
# -----------------------------------
# The query attribute of the QuerySet returns a Query object
all_entries.query  # <django.db.models.sql.query.Query at 0x...>

# The string representation of Query returns raw SQL
print all_entries.query
# SELECT "muzings_entry"."id", ...
#   FROM "muzings_entry"

#Retrieving ALL Records - Part Deux
#----------------------------------

for e in Entry.objects.all():
    print 'type(e): %s \n      e: %s' % (type(e), e)

# type(e): <class 'awesmblogz.muzings.models.Entry'>
#      e: 232 Sand dollars
# type(e): <class 'awesmblogz.muzings.models.Entry'>
#      e: Procrastination Hack : change and to or
#  ... rest truncated ...

# casting the QuerySet to a list, also returns a list
# of Entry instances
entries = list(Entry.objects.all())
e0 = entries[0]
e0  # <Entry: 232 Sand dollars>
type(e0)  # awesmblogz.muzings.models.Entry

# The column data can be accessed via the instance attributes
# with same name as the corresponding fields.
e0.title  # u'232 Sand Dollars'
e0.slug  # u'232-sand-dollars'
e0.date_created  # datetime.datetime(2011, 11, 15, 6, 32, tzinfo=<UTC>)

# Queries with a WHERE clause
# ----------------------------

# get() returns a single model instance
e = Entry.objects.get(title="232 Sand dollars")
e  # <Entry: 232 Sand dollars>
type(e)  # awesmblogz.muzings.models.Entry

# get() raises a MultipleObjectedReturned exception if more than
# one record matches the condition
Entry.objects.get(status=1)
# ... truncated ...
# MultipleObjectsReturned: get() returned more than one Entry --
# it returned 2! Lookup parameters were {'status': 1}

# get() raises a DoesNotExist exception if nothing matches the
# condition
Entry.objects.get(title='foo')
# DoesNotExist: Entry matching query does not exist.

# Examples of filter() method

entries_hidden_draft = Entry.objects.filter(status__lte=1)
list(entries_hidden_draft)
# [<Entry: 232 Sand dollars>,
#  <Entry: Procrastination Hack : change and to or>,
#   <Entry: After 15 years of practice...>,
#   <Entry: What do you hate not doing?>]

entries_in_2011 = Entry.objects.filter(status__year=2011)
list(entries_in_2011)
# [<Entry: 232 Sand dollars>,
#  <Entry: Procrastination Hack : change and to or>,
#  <Entry: Fish don't know they're in water>]

entries = Entry.objects.exclude(date_created__year=2011)
list(entries_in_2011)
# [<Entry: After 15 years of practice...>,
#  <Entry: Flip the stick>,
#  <Entry: What do you hate not doing?>,
#  <Entry: No more yes. It's either HELL YEAH! or no>,
#  <Entry: Ideas are just a multiplier of execution>]

# Refining queries by *chaining* queryset methods
# -----------------------------------------------

entries_2011 = Entry.objects.filter(date_created__year=2011)
type(entries_2011)  # django.db.models.query.QuerySet

# refine entries_2011 by chaining another queryset method
hid_dft_2011 = entries_2011.filter(status__lte=1)
# You can also do it in one step
hid_dft_2011 = (Entry.objects.filter(date_created__year=2011)
                             .filter(status__lte=1))
list(hid_dft_2011)
# [<Entry: 232 Sand dollars>,
#  <Entry: Procrastination Hack : change and to or>]

# You can only *chain* the methods as long as the result of the
# previous evaluation is a QuerySet instance.
# For example, the following is illegal; Entry.objects.get(pk=1)
# returns a model instance, not a QuerySet instance.

Entry.objects.get(id=1).filter(title__startswith='a')
#  ... truncated ...
#  AttributeError: 'Entry' object has no attribute 'filter'

# Refining by passing multiple keyword arguments
# ----------------------------------------------
# You can supply multiple keyword arguments to the filter(), get()
#  or ``exclude()`` methods, and in the resulting SQL WHERE clause,
# all the conditions will be AND-ed.
list(Entry.objects.filter(date_created__year=2011, status__lte=1))
# [<Entry: 232 Sand dollars>,
#   <Entry: Procrastination Hack : change and to or>]


# OR conditions using Q objects
# -----------------------------
from django.db.models import Q
entries = Entry.objects.filter(Q(date_created__year=2011) |
                               Q(status__lte=1))
list(entries)
# [<Entry: 232 Sand dollars>,
#  <Entry: Procrastination Hack : change and to or>,
#  <Entry: Fish don't know they're in water>,
#  <Entry: After 15 years of practice...>,
#  <Entry: What do you hate not doing?>]

# Q objects can be AND-ed with &, negated with ~ and OR-ed with |
Entry.objects.filter((Q(date_created__year=2011) |
                      Q(status__lte=1))
                     & (~ Q(title__startswith='P')))
# [<Entry: 232 Sand dollars>,
#  <Entry: Fish don't know they're in water>,
#  <Entry: After 15 years of practice...>,
#  <Entry: What do you hate not doing?>]

# There is more than one way to write a query. The above query is
# same as the one below
Entry.objects.filter(Q(date_created__year=2011) |
                     Q(status__lte=1)).exclude(title__startswith='P')
# [<Entry: What do you hate not doing?>,
#  <Entry: Fish don't know they're in water>,
#  <Entry: After 15 years of practice...>,
#  <Entry: 232 Sand dollars>]

# Retrieving only specific columns
# --------------------------------

# The follow query retrieves ALL the columns and then we use a
# list comprehension to get the specific columns
entries = Entry.objects.filter(title__startswith='F')
entry_title_statuses = [(e.title, e.status) for e in entries]
entry_title_statuses
# [(u"Fish don't know they're in water", 2),
#  (u'Flip the stick', 2)]

# values() returns a list of dictionaries with only the specific columns
entries = (Entry.objects.filter(title__startswith='F')
                        .values('title', 'status'))
type(entries)  # django.db.models.query.ValuesQuerySet
list(entries)
# [{'status': 2, 'title': u"Fish don't know they're in water"},
#  {'status': 2, 'title': u'Flip the stick'}]

# values_list() returns a list of tuples
entries = (Entry.objects.filter(title__startswith='F')
                        .values('title', 'status'))
type(entries)  # django.db.models.query.ValuesListQuerySet
list(entries)
# [(u"Fish don't know they're in water", 2),
#  (u'Flip the stick', 2)]

# Counting and Aggregating
# ------------------------

# Use the count method to issue a query with COUNT(*) SQL
Entry.objects.filter(status=1).count()  # 2
# SELECT COUNT(*) FROM "muzings_entry" WHERE "muzings_entry"."status" = 1
# Gotcha! Django does NOT query the db if the count can be evaluated locally.
entries = Entry.objects.all()
# Force the queryset to be evaluated
entries_list = list(entries)
# count is evaluated locally. No query to DB!
entries.count()

# Aggregations

from django.db.models import Max, Min
(Entry.objects.filter(status=1)
              .aggregate(Min('date_created'), max_dt=Max('date_created')))

# {'date_created__min':
#     datetime.datetime(2009, 8, 29, 3, 14, tzinfo=<UTC>),
#  'max_dt':
#     datetime.datetime(2010, 7, 3, 4, 55, 43, tzinfo=<UTC>)}

# Ordering and limiting
# ---------------------
entries = Entry.objects.order_by('status', '-title')
list(entries)

# [<Entry: Procrastination Hack : change and to or>,
#  <Entry: 232 Sand dollars>,
#  <Entry: What do you hate not doing?>,
#  <Entry: After 15 years of practice...>,
#  <Entry: No more yes. It's either HELL YEAH! or no>,
#  <Entry: Ideas are just a multiplier of execution>,
#  <Entry: Flip the stick>,
#  <Entry: Fish don't know they're in water>]

entries = Entry.objects.all()[2:5]
list(entries)
# [<Entry: Fish don't know they're in water>,
#  <Entry: After 15 years of practice...>,
#  <Entry: Flip the stick>]
type(entries)  # django.db.models.query.QuerySet

# Gotcha! Be careful if you use the step parameter of slicing syntax.
entries = Entry.objects.all()[2:5:1]
entries
# [<Entry: Fish don't know they're in water>,
#  <Entry: After 15 years of practice...>,
#  <Entry: Flip the stick>]

# Watch out! entries is not a QuerySet!
type(entries)  # list
