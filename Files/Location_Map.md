
'Brisbane - East,Queensland',
 'Brisbane - North,Queensland', 
 'Brisbane - South,Queensland',
 'Brisbane - West,Queensland',
 'Brisbane Inner City,Queensland',
 **'Cairns,Queensland',**  [Cairns and Hinterland]
 **'Darling Downs - Maranoa,Queensland',** [Darling Downs]
 'Fitzroy,Queensland', 
 **'Gold Coast,Queensland',** [Gold Coast]
 'Ipswich,Queensland',
 'Logan - Beaudesert,Queensland',
 **'Mackay,Queensland',** [Mackay]
 'Moreton Bay - North,Queensland',
 'Moreton Bay - South,Queensland',
 'Queensland - Outback,Queensland',
 **'Sunshine Coast,Queensland',** [Sunshine Coast]
 'Toowoomba,Queensland',
 **'Townsville,Queensland',** [Townsville]
 **'Wide Bay,Queensland'** [Wide Bay]





| Tropical                  | Central                   | Southern          |
| ------------------------- | ------------------------- | ----------------- |
| Torres and Cape           | **Central Queensland**  ? | **Metro South**   |
| **Cairns and Hinterland** | Central West              | **Darling Downs** |
| North West                | **Wide Bay**              | **West Moreton**  |
| **Townsville**            | **Sunshine Coast**        | South West        |
| **Mackay**                | **Metro North**           | **Gold Coast**    |



step1 :

change 

```
'Brisbane - East,Queensland',
 'Brisbane - North,Queensland', 
 'Brisbane - South,Queensland', 
 'Brisbane - West,Queensland',
 'Brisbane Inner City,Queensland',
```

to

```
Brisbane
```

change

```
 'Moreton Bay - North,Queensland',
 'Moreton Bay - South,Queensland',
```

to

```
Moreton
```

step 2:

```
Metro North\Metro South -> Brisbane
West Moreton -> Moreton
Cairns and Hinterland -> Cairns
Townsville -> Townsville
Mackay -> Mackay
Wide Bay -> Wide Bay
Sunshine Coast -> Sunshine Coast
Darling Downs - Maranoa -> Darling Downs
Gold Coast -> Gold Coast
Central Queensland -> Fitzroy
```

