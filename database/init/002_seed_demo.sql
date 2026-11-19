WITH demo_project AS (
    INSERT INTO projects (name, description, cut_off_date)
    SELECT 'Proyecto Demo Trycore', 'Proyecto de demostración con tres actividades para validar los indicadores EVM.', CURRENT_DATE
    WHERE NOT EXISTS (
        SELECT 1 FROM projects WHERE name = 'Proyecto Demo Trycore'
    )
    RETURNING id
)
INSERT INTO activities (
    project_id,
    name,
    bac,
    planned_progress,
    actual_progress,
    actual_cost
)
SELECT
    demo_project.id,
    activity.name,
    activity.bac,
    activity.planned_progress,
    activity.actual_progress,
    activity.actual_cost
FROM demo_project
CROSS JOIN (
    VALUES
        ('Diseño', 10000000.00, 60.00, 50.00, 7000000.00),
        ('Desarrollo', 30000000.00, 40.00, 35.00, 12000000.00),
        ('Pruebas', 15000000.00, 20.00, 10.00, 2000000.00)
) AS activity(name, bac, planned_progress, actual_progress, actual_cost)
WHERE NOT EXISTS (
    SELECT 1
    FROM activities
    WHERE project_id = demo_project.id
);
