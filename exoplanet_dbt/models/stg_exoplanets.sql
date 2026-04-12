SELECT
    pl_name                          AS nombre_planeta,
    hostname                         AS estrella,
    pl_masse                         AS masa_terrestre,
    pl_rade                          AS radio_terrestre,
    pl_orbper                        AS periodo_orbital_dias,
    pl_eqt                           AS temperatura_k,
    st_teff                          AS temperatura_estrella_k,
    discoverymethod                  AS metodo_descubrimiento,
    CAST(disc_year AS INTEGER)        AS año_descubrimiento,
    CASE
        WHEN pl_eqt BETWEEN 200 AND 320 
         AND pl_rade <= 1.5           THEN 'Habitable'
        WHEN pl_rade <= 1.5           THEN 'Rocoso'
        WHEN pl_rade <= 4             THEN 'Super-Tierra'
        WHEN pl_rade <= 10            THEN 'Gigante gaseoso'
        ELSE                               'Gigante extremo'
    END                              AS tipo_planeta

FROM exoplanets
WHERE pl_name IS NOT NULL