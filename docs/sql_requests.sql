SELECT club_id, COUNT(*) FROM public.record_club_person GROUP BY club_id ORDER BY COUNT(*) DESC;
