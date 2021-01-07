SELECT club_id, COUNT(*) FROM public.record_club_person GROUP BY club_id HAVING COUNT(*) > 5 ORDER BY COUNT(*) DESC;

SELECT account_name
FROM (((SELECT club_id FROM public.record_club_person 
GROUP BY club_id HAVING COUNT(*) > 5) AS clubs
INNER JOIN public.record_club_person ON public.record_club_person.club_id = clubs.club_id)
INNER JOIN public.person ON public.person.person_id = public.record_club_person.person_id);

SELECT *
FROM (public.person
INNER JOIN public.record_club_person
ON public.person.person_id = public.record_club_person.person_id)
WHERE club_id = 11353;

SELECT *
FROM (public.person
INNER JOIN public.record_club_person
ON public.person.person_id = public.record_club_person.person_id)
WHERE club_id IN (SELECT club_id FROM public.record_club_person GROUP BY club_id HAVING COUNT(*) > 5 ORDER BY RANDOM() LIMIT 1)
ORDER BY RANDOM() LIMIT 2;
