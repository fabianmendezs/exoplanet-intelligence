SELECT
    nombre_planeta,
    estrella,
    tipo_planeta,
    radio_terrestre,
    masa_terrestre,
    temperatura_k,
    año_descubrimiento,
    RANK() OVER (
        PARTITION BY tipo_planeta 
        ORDER BY radio_terrestre
    )                                   AS ranking_en_tipo,
    ROUND(AVG(radio_terrestre) OVER (
        PARTITION BY tipo_planeta
    ), 2)                               AS radio_promedio_tipo,
    COUNT(*) OVER (
        PARTITION BY tipo_planeta
    )                                   AS total_en_tipo

FROM {{ ref('stg_exoplanets') }}
WHERE radio_terrestre IS NOT NULL