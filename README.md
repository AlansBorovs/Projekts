### Projekts Automatizēta PDF failu lejupielāde un informācijas lasīšana no tiem, lai samaksātu par internetu.
Tātad, būtībā, tas ir mans projekts, pie kura es strādāju, tas automatizē manu mēneša maksājumu par internetu. Tas izmanto Gmail API, lai piekļūtu manam gmail un pārlūko manas e-pastus, kas nāk no rekins@elektrons-k.lv, tad tas izvēlas jaunāko un lejupielādē pdf failu, kas satur manu rēķinu, proti, cik daudz man jāmaksā par internetu. Tas viss notiek "fetch_a_pdf_file_from_gmail.py", savukārt otrs skripts "pdfreader_swedbank.py" tiek izmantots, lai lasītu lejupielādēto pdf failu, lai iegūtu informāciju par to, cik daudz man jāmaksā un līdz kuram laikam man jāmaksā par to, pēc šīs informācijas iegūšanas parādās windows ziņojumu lodziņš, kas jautā, vai man vajadzētu to maksāt tūlīt vai nē, spiežot jā, tas aizved mani uz swedbank vietni, kur es tad par to maksāju, spiežot nē, būtu jāiestata atgādinājums, kas man atgādinātu 4-5 dienas pirms apmaksas termiņa beigas, bet es to vēl neesmu ieviesis.<br>
## Ka kods strada
```fetch_a_pdf_file_from_gmail.py```
Šis ir Python skripts, kas izmanto Google Gmail API, lai meklētu un lejupielādētu PDF failus no mana Gmail konta. Šeit ir detalizēts apraksts par to, kā tas darbojas:

Skripts sākumā importē nepieciešamās bibliotēkas un definē ```SCOPES kā ‘https://mail.google.com/’,``` kas ir nepieciešams, lai piekļūtu Gmail API. Tad tiek definēta galvenā funkcija ```main()```, kurā notiek visa skripta darbība.

Funkcijā ```main()``` skripts pārbauda, vai fails ```token.json``` eksistē un vai tajā esošās kredenciālas ir derīgas. Ja fails ```token.json``` eksistē, skripts ielādē kredenciālas no tā. Ja kredenciālas ir derīgas, bet ir beigušās, tās tiek atjaunotas. Ja kredenciālas neeksistē vai nav derīgas, skripts izveido jaunas kredenciālas. Kredenciālas tiek saglabātas failā ```token.json.```

Pēc tam, izmantojot kredenciālas, skripts izveido Gmail servisu. Ar šo servisu skripts veic meklēšanu Gmail, meklējot ziņojumus no ‘rekins@elektrons-k.lv’. Ja nav jaunu ziņojumu, skripts izdrukā atbilstošu ziņojumu. Ja ir ziņojumi, skripts iegūst pirmo ziņojumu.

Skripts iegūst ziņojuma ‘payload’ un ‘headers’. No ‘headers’ tiek iegūts ziņojuma datums. Tiek iegūtas arī ziņojuma daļas no ‘payload’. Katra daļa tiek pārbaudīta, lai redzētu, vai tā ir PDF vai okteta plūsma. Ja tā ir, tiek iegūti dati no tās.

Ja dati ir pieejami, tie tiek dekodēti un saglabāti kā PDF fails. Fails tiek saglabāts norādītajā ceļā jūsu datorā. Skripts izdrukā ziņojumu par to, ka fails ir veiksmīgi lejupielādēts, un parāda pop-up ziņojumu par lejupielādes pabeigšanu.

1. ```os:``` Šī bibliotēka tiek izmantota, lai nodrošinātu operētājsistēmas atkarīgas funkcionalitātes, piemēram, failu un direktoriju darbības.

2. ```base64:``` Šī bibliotēka tiek izmantota, lai dekodētu base64 kodētus datus.

3. ```ctypes:``` Šī bibliotēka tiek izmantota, lai parādītu pop-up ziņojumus Windows operētājsistēmā.

4. ```google.oauth2.credentials:``` Šī bibliotēka tiek izmantota, lai ielādētu kredenciālas no faila token.json.

5. ```google_auth_oauthlib.flow:``` Šī bibliotēka tiek izmantota, lai izveidotu jaunas kredenciālas.

6. ```google.auth.transport.requests:``` Šī bibliotēka tiek izmantota, lai atjaunotu kredenciālas.

7. ```googleapiclient.discovery:``` Šī bibliotēka tiek izmantota, lai izveidotu Gmail servisu.


<br> ```pdfreader_swedbank.py``` Šis skripts ir paredzēts, lai lasītu PDF failu, izvilktu no tā konkrētu informāciju un pēc tam izmantotu šo informāciju, lai izveidotu maksājumu vai atgādinājumu par maksājumu.

Skripts vispirms pārbauda, vai konkrēts PDF fails eksistē norādītajā direktorijā.
Ja fails eksistē, skripts izvelk tekstu no PDF faila.
Skripts pēc tam aizstāj nepareizās rakstzīmes izvilkta tekstā.
No izvilkta teksta tiek atrasta kopējā jāmaksājamā summa un maksājuma termiņš.
Tiek izveidots ziņojums par uznirstošo atgādinājumu, kas ietver jāmaksājamās summas un maksājuma termiņa informāciju.
Tiek izveidots uznirstošais logs ar ziņojumu un opcijām maksāt tagad vai vēlāk.
Ja lietotājs izvēlas maksāt tagad, skripts atver Swedbank tīmekļa vietni.

1. ```os:``` Izmanto, lai interaktīvi darbotos ar operētājsistēmu, piemēram, uzskaitītu failus direktorijā.

2. ```webbrowser:``` Izmanto, lai atvērtu tīmekļa lapu jaunā pārlūka logā.

3. ```datetime``` un ```dateutil.relativedelta:``` Izmanto, lai strādātu ar datumiem un laikiem.

4. ```pdfminer.high_level:``` Izmanto, lai izvilkta tekstu no PDF faila.

5. ```ctypes:``` Izmanto, lai izveidotu uznirstošo logu ar pielāgotu ziņojumu un opcijām.