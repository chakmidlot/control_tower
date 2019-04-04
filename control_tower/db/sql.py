INITIALIZE_DB = '''
create table if not exists telegram_users (
  id serial primary key,
  telegram_user_id int,
  device_id varchar(256)
);
create index if not exists telegram_users_user_id on telegram_users (device_id);
create unique index if not exists telegram_users_user_device on telegram_users (telegram_user_id, device_id);

create table if not exists last_level (
    id serial primary key,
    device_id varchar(256) unique,
    level smallint
);
create index if not exists last_level_device_id on last_level (device_id);
'''


SELECT_LEVEL_SQL = '''
select "level"
  from last_level
  where device_id = %s;
'''

INSERT_USER_SQL = '''
insert into telegram_users (telegram_user_id, device_id)
  values (%s, %s)
  on conflict do nothing;
'''

SET_LEVEL_SQL = '''
insert into last_level (device_id, "level")
  values (%s, %s)
  on conflict (device_id) do update set "level" = %s;
'''

SELECT_USERS_SQL = '''
select telegram_user_id
  from telegram_users
  where device_id = %s;
'''

SELECT_USER_DEVICES_SQL = '''
select device_id
  from telegram_users
  where telegram_user_id = %s;
'''

DELETE_DEVIDE = '''
delete from telegram_users 
  where device_id = %s 
  and telegram_user_id = %s;
'''

DELETE_ALL_DEVIDES = '''
delete from telegram_users 
  where telegram_user_id = %s;
'''