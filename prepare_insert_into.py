# Event Data less than 5 minutes, excluding 'honeyserver' entities on the matching set
insert_event_data_lt5m = """insert into event_data_lt5m
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.entity <> 'honeyserver')
where
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 0 and
    EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 300
order by edm.timestamp)
;
"""
# Event Data less than 5 minutes only looking at 'honeyservers' on the original set, matching everything excluding 'repeat offenders'
insert_event_data_lt5m_honeyserver = """insert into event_data_lt5m_honeyserver
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.eventclass <> 'Suspicious and persistant')
where
	edm.entity = 'honeyserver' and
	edm.eventclass <> 'Suspicious and persistant' and
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and
    EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 0 and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 300
order by edm.timestamp)
;
"""
# Event Data less than 5 minutes excluding 'honeyservers' on the original set, matching everything excluding 'repeat offenders'
insert_event_data_lt5m_no_ro = """insert into event_data_lt5m_no_ro
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.eventclass <> 'Suspicious and persistant')
where
	edm.entity <> 'honeyserver' and
	edm.eventclass <> 'Suspicious and persistant' and
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and
    EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 0 and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 300
order by edm.timestamp)
;
"""
# Event Data equal to or greather than 5 minutes and less than 48 hours, excluding 'honeyserver' entities on the matching set
insert_event_data_5mtolt48h = """insert into event_data_5mtolt48h
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.entity <> 'honeyserver')
where
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 300 and 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 172800
order by edm.timestamp)
;
"""

# Event Data equal to or greather than 5 minutes and less than 48 hours only looking at 'honeyservers' on the original set, matching everything excluding 'repeat offenders'
insert_event_data_5mtolt48h_honeyserver = """insert into event_data_5mtolt48h_honeyserver
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.eventclass <> 'Suspicious and persistant')
where
	edm.entity = 'honeyserver' and
	edm.eventclass <> 'Suspicious and persistant' and
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 300 and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 172800
order by edm.timestamp)
;
"""

# Event Data equal to or greather than 5 minutes and less than 48 hours excluding 'honeyservers' on the original set, matching everything excluding 'repeat offenders'
insert_event_data_5mtolt48h_no_ro = """insert into event_data_5mtolt48h_no_ro
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.eventclass <> 'Suspicious and persistant')
where
	edm.entity <> 'honeyserver' and
	edm.eventclass <> 'Suspicious and persistant' and
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 300 and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 172800
order by edm.timestamp)
;
"""
# Event Data for this first 48 hours, excluding 'honeyserver' entities on the matching set
insert_event_data_first48h = """insert into event_data_first48h
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.entity <> 'honeyserver')
where
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and
    EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 0 and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 172800
order by edm.timestamp)
;
"""
# Event Data for this first 48 hours only looking at 'honeyservers' on the original set, matching everything excluding 'repeat offenders'
insert_event_data_first48h_honeyserver = """insert into event_data_first48h_honeyserver
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.eventclass <> 'Suspicious and persistant')
where
	edm.entity = 'honeyserver' and
	edm.eventclass <> 'Suspicious and persistant' and
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and 
    EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 0 and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 172800
order by edm.timestamp)
;
"""
# Event Data for this first 48 hours excluding 'honeyservers' on the original set, matching everything excluding 'repeat offenders'
insert_event_data_first48h_no_ro = """insert into event_data_first48h_no_ro
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.eventclass <> 'Suspicious and persistant')
where
	edm.entity <> 'honeyserver' and
	edm.eventclass <> 'Suspicious and persistant' and
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and
    EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 0 and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 172800
order by edm.timestamp)
;
"""
# Event Data equal to or greather than 48 hours and less than 7 days, excluding 'honeyserver' entities on the matching set
insert_event_data_48htolt7d = """insert into event_data_48htolt7d
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.entity <> 'honeyserver')
where
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 172800 and 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 604800
order by edm.timestamp)
;
"""
# Event Data equal to or greather than 48 hours and less than 7 days, only looking at 'honeyservers' on the original set, matching everything excluding 'repeat offenders'
insert_event_data_48htolt7d_honeyserver = """insert into event_data_48htolt7d_honeyserver
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.eventclass <> 'Suspicious and persistant')
where
	edm.entity = 'honeyserver' and
	edm.eventclass <> 'Suspicious and persistant' and
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 172800 and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 604800
order by edm.timestamp)
;
"""
# Event Data equal to or greather than 48 hours and less than 7 days, excluding 'honeyservers' on the original set, matching everything excluding 'repeat offenders'
insert_event_data_48htolt7d_no_ro = """insert into event_data_48htolt7d_no_ro
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.eventclass <> 'Suspicious and persistant')
where
	edm.entity <> 'honeyserver' and
	edm.eventclass <> 'Suspicious and persistant' and
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 172800 and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) < 604800
order by edm.timestamp)
;
"""
# Event Data 7 days or more, excluding 'honeyserver' entities on the matching set
insert_event_data_7dormore = """insert into event_data_7dormore 
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.entity <> 'honeyserver')
where
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 604800
order by edm.timestamp);
"""
# Event Data 7 days or more looking at 'honeyservers' on the original set, matching everything excluding 'repeat offenders'
insert_event_data_7dormore_honeyserver = """insert into event_data_7dormore_honeyserver
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.eventclass <> 'Suspicious and persistant')
where
	edm.entity = 'honeyserver' and
	edm.eventclass <> 'Suspicious and persistant' and
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 604800
order by edm.timestamp)
;
"""
# Event Data 7 days or more excluding 'honeyservers' on the original set, matching everything excluding 'repeat offenders'
insert_event_data_7dormore_no_ro = """insert into event_data_7dormore_no_ro
(orig_sourceip,
orig_timestamp, 
orig_eventclass,
orig_entity, 
match_timestamp, 
match_eventclass, 
match_entity, 
match_destinationip, 
match_destinationport, 
timedelta)
(select
    edm.sourceip,
	edm.timestamp, 
	edm.eventclass,
	edm.entity,
	eds.timestamp,
	eds.eventclass,
	eds.entity,
	eds.destinationip,
	eds.destinationport, 
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) as timedelta
from event_data_import as edm
left join event_data_import as eds 
on (edm.sourceip = eds.sourceip and eds.timestamp > edm.timestamp and eds.eventclass <> 'Suspicious and persistant')
where
	edm.entity <> 'honeyserver' and
	edm.eventclass <> 'Suspicious and persistant' and
	edm.timestamp  >= '2018-08-01' and 
	edm.timestamp < '2018-11-01' and
	EXTRACT(EPOCH FROM (eds.timestamp - edm.timestamp)) >= 604800
order by edm.timestamp)
;
"""