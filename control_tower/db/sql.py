#  
#                                     sync_tokens
#                                     =============
#                                     device_id     ---+
#                                     token            |
#  telegram_dialogs                   creation_time    |
#  ================                                    |
#  telegram_id      --+                                |
#  command_id         |                                |
#  message_time       |                                |
#  data               |                                |
#                     |  +--> devices      <-----------+
#                     |  |    ============
#  telegram_users <---+  |    device_id
#  ==============        |    name
#  telegram_id           |    charge_level
#  device_id      -------+    update_time
#  

INITIALIZE_DB = '''
create table if not exists devices (
    device_id serial primary key,
    device_code varchar(256) unique,
    device_name varchar(60),
    charge_level smallint,
    update_time timestamp
);

create table if not exists telegram_users (
  telegram_user_id int,
  device_id int
);
create index if not exists telegram_users_device_id
    on telegram_users (device_id);
create index if not exists telegram_users_user_id
    on telegram_users (telegram_user_id);
create unique index if not exists telegram_users_user_device
    on telegram_users (telegram_user_id, device_id);

create table if not exists sync_tokens (
    device_id int,
    token varchar(256),
    creation_time timestamp
);
create index if not exists sync_tokens_creation_time
    on sync_tokens (creation_time);

create table if not exists telegram_dialogs (
    telegram_id int,
    command_id int,
    message_time timestamp,
    data varchar(256)
);
create index if not exists telegram_dialogs_telegram_id
    on telegram_dialogs (telegram_id);
'''

INSERT_DEVICE = '''
insert into devices (device_code, device_name)
  values (%s, %s);
'''

SELECT_LEVEL_BY_NAME_AND_TELEGRAM_SQL = '''
select charge_level
  from devices
  left join telegram_users
    using (device_id)
  where device_name = %s
    and telegram_user_id = %s;
'''

SELECT_LEVEL_BY_DEVICE_ID_SQL = '''
select charge
  from battery_charges
  where device_id = %s;
'''

UPDATE_CHARGE_BY_CODE_SQL = '''
update devices
  set charge_level = %s,
      update_time = now()
  where device_code = %s;
'''

UPDATE_DEVICE_NAME_SQL = '''
update devices
  set device_name = %s
  where device_id = %s;
'''

INSERT_USER_SQL = '''
insert into telegram_users (telegram_user_id, device_id)
    select %s, device_id
      from devices
      where device_code = %s
  on conflict do nothing;
'''

SELECT_TELEGRAM_USERS_BY_DEVICE_ID_SQL = '''
select telegram_user_id
  from telegram_users
  where device_id = %s;
'''

SELECT_USER_DEVICES_SQL = '''
select device_name
  from telegram_users
  left join devices
    using (device_id)
  where telegram_user_id = %s;
'''

DELETE_DEVICE_FOR_TELEGRAM_SQL = '''
delete from telegram_users 
  using devices
  where telegram_users.device_id = devices.device_id
    and device_name = %s and telegram_user_id = %s;
'''

DELETE_ALL_DEVIDES_FOR_TELEGRAM_SQL = '''
delete from telegram_users 
  where telegram_user_id = %s;
'''

DELETE_DEVICE = '''
delete from devices
  where device_code = %s;
'''
