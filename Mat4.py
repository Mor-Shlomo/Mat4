

import requests
dic=dict()
address1="תל אביב"
api_key='בקובץ'
file=open("dests.txt", encoding='utf8')
for line in file :
    try:
        address2=line.strip()
        urlA="https://maps.googleapis.com/maps/api/distancematrix/json?key=%s&origins=%s&destinations=%s"%(api_key,address1,address2)
        try:
            response=requests.get(urlA)
            if not response.status_code== 200:
                print("HTTP error", response.status_code)
            else:
                try:
                    response_data=response.json()
                except:
                    print("Response not in valid JSON format")
        except:
            print("Something went wrong with requests.get")            
        distance_TLV=response_data['rows'][0]['elements'][0]['distance']['text']
    except:
        print("wrong")
        continue
    km=distance_TLV.find('km')
    if km<1:
        m=response_data['rows'][0]['elements'][0]['distance']['value']
        distance_TLV= str(m/1000)+" km"    
    time=response_data['rows'][0]['elements'][0]['duration']['value']
    time_s=time
    hours=int(time/(3600))
    mins=round((time-3600*hours)/60)
    if hours>=1:
        time_s=str(hours)+" hours "+str(mins)+" mins" 
    else:
        time_s=str(mins)+" mins"
  
    urlB="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" %( address2,api_key)
    try:
        response=requests.get(urlB)
        if not response.status_code==200:
            print("HTTP error", response.status_code)
        else:
            try:
                response_data_2=response.json()
            except:
                print("Response not in valid JSON format")
    except:
        print("Something went wrong with requests.get")
    
    longitude= response_data_2['results'][0]['geometry']['location']['lng']
    latitude= response_data_2['results'][0]['geometry']['location']['lat']        
    tuple1=('distance from Tel Aviv: '+distance_TLV, 'Time from Tel Aviv: '+time_s, 'longitude: '+str(longitude), 'latitude: '+str(latitude))
    dic[address2]=tuple1

for address in dic:
    print("city:", address)
    print(dic[address][0])
    print(dic[address][1])
    print(dic[address][2])
    print(dic[address][3])
    print()

dic_d=dict()
for address in dic:
    d=dic[address][0].split()
    distance=float(d[4].replace(",",""))
    dic_d[address]=distance
lst=sorted([(distance,address)for address, distance in dic_d.items() ] ,reverse=True)
print("The 3 cities furthest from Tel Aviv ")
for distance,address in lst[:3]:
    print (address,distance)