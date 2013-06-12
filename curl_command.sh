#!/bin/bash
curl -k --request POST --header "Content-Type: text/xml;charset=UTF-8;"  -H "SOAPAction: "urn:mediate";" --data @PATH_HOME/Work/p12request_tmp.xml https://xx.xx.it/te/processes/STD_QDS_CertificateRetrievalST.STD_QDS_pippo  > PATH_HOME/Work/curl_result.xml   2> /dev/null
