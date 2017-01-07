#!/bin/bash

while read url
	do
		echo '{"domain":"piata-az","url":"'$url'"}'
	done
