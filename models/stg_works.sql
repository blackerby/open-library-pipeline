with
    works as (
        select `key`, title, subjects, author
        from `open-library-pipeline.open_library.works` works
        cross join unnest(authors) as author
    )
select *
from works
