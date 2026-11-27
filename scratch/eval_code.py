
import dis, sys, traceback
try:
    import BigWorld
    import mobile.entities.Athlete
    fn = mobile.entities.Athlete.Athlete.onUpdateLuckyCarnivalData
    print('CO_NAMES:', fn.__code__.co_names)
    print('CO_VARNAMES:', fn.__code__.co_varnames)
    print('CO_CONSTS:', fn.__code__.co_consts)
except Exception as e:
    print('Error:', e)
    traceback.print_exc()
