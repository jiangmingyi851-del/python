def solution(season, dayCount, initialPhase):
    dic={'NewMoon':0,'Crescent':1,'Quarter':2,'Gibbous':3,'Full':4,'Waning':5,'Eclipse':6,'Twilight':7}
    dic_to_phase={'0':'NewMoon','1':'Crescent','2':'Quarter','3':'Gibbous','4':'Full','5':'Waning','6':'Eclipse','7':'Twilight'}
    day=0
    if season=='February':
        day+=31
    if season=='March':
        day+=59
    if season=='April':
        day+=90
    if season=='May':
        day+=120
    if season=='June':
        day+=151
    if season=='July':
        day+=181
    if season=='August':
        day+=212
    if season=='September':
        day+=243
    if season=='October':
        day+=273
    if season=='November':
        day+=304
    if season=='December':
        day+=334
    day+=dayCount
    phase=dic[initialPhase]
    ans=(day+phase-1)%8
    return dic_to_phase[str(ans)]
