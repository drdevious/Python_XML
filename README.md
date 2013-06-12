Python_XML
==========

read xml for SOAP request and store the reply on cvs

Questo script parte da un template xml e da un file di dati così formato :
CADF000001|p.pippo|111111

Dopo aver formattato l'xml, lo passa ad uno script bash che si occupa di fare una richiesta soap ad una webservices.
La risposta xml del server viene verificata e storicizzata in un file csv.
