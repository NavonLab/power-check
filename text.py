import gammu
from phonebook import phonebook

#configure gammu 
state_machine =  gammu.StateMachine()
state_machine.ReadConfig()
state_machine.Init()

#send message to all numbers in phonebook when the power goes out
def power_out():
    out_message = {
        'Text': 'URGENT: Power outage in SPL has been recorded.',
        'SMSC': {'Location': 1},
    }
    for name, [number, email] in phonebook.items():
        out_message['Number'] = number
        state_machine.SendSMS(out_message)

#send message to all numbers in phonebook when the power is restored
def power_restored():
        restored_message = {
                'Text': 'Power has been restored in SPL.',
                'SMSC': {'Location': 1},
        }
        for name, [number, email] in phonebook.items():
                restored_message['Number'] = number
                state_machine.SendSMS(restored_message)

