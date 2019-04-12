#! /bin/bash

wget 					\
	--recursive \
	--page-requisites \
	--convert-links \
	--no-clobber \
	--no-parent \
	--html-extension \
	--domains spanishdict.com \
	--continue \
	--exclude-directories='/lists,/quizzes,/users,/examples,/social,/company,/verbos,/traductor,/guia' \
		www.spanishdict.com/
		
