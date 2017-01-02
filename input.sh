#!/bin/bash

cat urls | while read url
do
	echo '{"domain":"piata-az","url":"'$url'"}'
done