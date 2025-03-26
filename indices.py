# sentinel2_indices.py


INDEX_NAMES = [
    "arvi",  # Atmospherically Resistant Vegetation Index
    "bi",  # brightness Index
    "bi2",  # Brightness Index 2
    "ci",  # Chlorophyll Index
    "dvi",  # Difference Vegetation Index
    "gemi",  # Global Environment Monitoring Index
    "gndvi",  # Green Normalized Difference Vegetation Index
    "ipvi",  # Infrared Percentage Vegetation Index
    "ireci",  # Infrared Ratio Vegetation Index
    "mcari",  # Modified Chlorophyll Absorption Ratio Index
    "mndwi",  # Modified Normalized Difference Water Index
    "msavi2",  # Modified Soil-Adjusted Vegetation Index 2
    "mtci",  # Meris Terrestrial Chlorophyll Index
    "dni45",  # Drought Normalized Index 45
    "ndpi",  # Normalized Difference Plant Index
    "ndti",  # Normalized Difference Tillage Index
    "ndwi",  # Normalized Difference Water Index
    "ndwi2",  # Normalized Difference Water Index 2
    "pssra",  # Plant Stress Severity Ratio a
    "reip",  # Red Edge Inflection Point
    "ri",  # Ratio Index
    "ndvi",  # Normalized Difference Vegetation Index
    "savi",  # Soil-Adjusted Vegetation Index
    "tndvi",  # Transformed Normalized Difference Vegetation Index
    "vi",  # vegetation index
]


def add_arvi(image):
    """
    Compute Atmospherically Resistant Vegetation Index (ARVI) using the formula:

    ARVI = (NIR - rb) / (NIR + rb)

    Where:
    rb = R - γ * (B - R) (with γ set to 1)
    NIR = B8 (Near-Infrared Band)
    R = B4 (Red Band)
    B = B2 (Blue Band)
    """
    gamma = 1
    rb = image.expression(
        "red - gamma * (blue - red)",
        {
            "red": image.select("B4"),
            "blue": image.select("B2"),
            "gamma": gamma,
        },
    )
    arvi = image.expression(
        "(nir - rb) / (nir + rb)",
        {
            "nir": image.select("B8"),
            "rb": rb,
        },
    )
    return image.addBands(arvi.rename("arvi"))


def add_bi(image):
    """
    Compute Brightness Index (BI) using the formula:

    BI = sqrt((R^2 + G^2) / 2)

    Where:
    R = B4 (Red Band)
    G = B3 (Green Band)
    """
    bi = image.expression(
        "sqrt((red * red + green * green) / 2)",
        {
            "red": image.select("B4"),
            "green": image.select("B3"),
        },
    )
    return image.addBands(bi.rename("bi"))


def add_bi2(image):
    """
    Compute Brightness Index 2 (BI2) using the formula:

    BI2 = sqrt((R^2 + G^2 + NIR^2) / 3)

    Where:
    R = B4 (Red Band)
    G = B3 (Green Band)
    NIR = B8 (Near-Infrared Band)
    """
    bi2 = image.expression(
        "sqrt((red * red + green * green + nir * nir) / 3)",
        {
            "red": image.select("B4"),
            "green": image.select("B3"),
            "nir": image.select("B8"),
        },
    )
    return image.addBands(bi2.rename("bi2"))


def add_ci(image):
    """
    Compute Chlorophyll Index (CI) using the formula:

    CI = (R - G) / (R + G)

    Where:
    R = B4 (Red Band)
    G = B3 (Green Band)
    """
    ci = image.expression(
        "(red - green) / (red + green)",
        {
            "red": image.select("B4"),
            "green": image.select("B3"),
        },
    )
    return image.addBands(ci.rename("ci"))


def add_dvi(image):
    """
    Compute Difference Vegetation Index (DVI) using the formula:

    DVI = NIR - R

    Where:
    NIR = B8 (Near-Infrared Band)
    R = B4 (Red Band)
    """
    dvi = image.expression(
        "nir - red",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
        },
    )
    return image.addBands(dvi.rename("dvi"))


# def add_gemi(image):
#     """
#     Compute Global Environment Monitoring Index (GEMI) using the formula:

#     GEMI = η * (1 - 0.25 * η) - ((B4 - 0.125) / (1 - B4))

#     Where:
#     η = (2 * (B8^2 - B4^2) + 1.5 * B8 + 0.5 * B4) / (B8 + B4 + 0.5)
#     NIR = B8 (Near-Infrared Band)
#     R = B4 (Red Band)
#     """
#     eta = image.expression(
#         "(2 * (nir * nir - red * red) + 1.5 * nir + 0.5 * red) / (nir + red + 0.5)",
#         {
#             "nir": image.select("B8"),
#             "red": image.select("B4"),
#         },
#     )
#     gemi = image.expression(
#         "eta * (1 - 0.25 * eta) - ((red - 0.125) / (1 - red))",
#         {
#             "eta": eta,
#             "red": image.select("B4"),
#         },
#     )

#     return image.addBands(gemi.rename("gemi"))


def add_gemi(image):
    """
    Compute Global Environment Monitoring Index (GEMI) using the formula:

    GEMI = η * (1 - 0.25 * η) - ((B4 - 0.125) / (1 - B4))

    Where:
    η = (2 * (B8^2 - B4^2) + 1.5 * B8 + 0.5 * B4) / (B8 + B4 + 0.5)
    NIR = B8 (Near-Infrared Band)
    R = B4 (Red Band)
    """
    gemi = image.expression(
        "((2 * (nir * nir - red * red) + 1.5 * nir + 0.5 * red) / (nir + red + 0.5)) * "
        "(1 - 0.25 * ((2 * (nir * nir - red * red) + 1.5 * nir + 0.5 * red) / (nir + red + 0.5))) - "
        "((red - 0.125) / (1 - red))",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
        },
    )
    return image.addBands(gemi.rename("gemi"))


def add_gndvi(image):
    """
    Compute Green Normalized Difference Vegetation Index (GNDVI) using the formula:

    GNDVI = (B8 - B3) / (B8 + B3)

    Where:
    NIR = B8 (Near-Infrared Band)
    G = B3 (Green Band)
    """
    gndvi = image.expression(
        "(nir - green) / (nir + green)",
        {
            "nir": image.select("B8"),
            "green": image.select("B3"),
        },
    )
    return image.addBands(gndvi.rename("gndvi"))


def add_ipvi(image):
    """
    Compute Infrared Percentage Vegetation Index (IPVI) using the formula:

    IPVI = B8 / (B8 + B4)

    Where:
    NIR = B8 (Near-Infrared Band)
    R = B4 (Red Band)
    """
    ipvi = image.expression(
        "nir / (nir + red)",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
        },
    )
    return image.addBands(ipvi.rename("ipvi"))


def add_ireci(image):
    """
    Compute Infrared Ratio Vegetation Index (IRECI) using the formula:

    IRECI = (RE - R) / (NIR / SIW)

    Where:
    RE = B7 (Red-Edge Band)
    R = B4 (Red Band)
    NIR = B5 (Near-Infrared Band)
    SIW = B6 (Shortwave Infrared Band)
    """
    ireci = image.expression(
        "(re - r) / (nir / siw)",
        {
            "re": image.select("B7"),
            "r": image.select("B4"),
            "nir": image.select("B5"),
            "siw": image.select("B6"),
        },
    )
    return image.addBands(ireci.rename("ireci"))


def add_mcari(image):
    """
    Compute Modified Chlorophyll Absorption Ratio Index (MCARI) using the formula:

    MCARI = ((B5 - B4) - 0.2 * (B5 - B3)) * (B5 / B4)

    Where:
    B5 = NIR (Near-Infrared Band)
    B4 = R (Red Band)
    B3 = G (Green Band)
    """
    mcari = image.expression(
        "((nir - red) - 0.2 * (nir - green)) * (nir / red)",
        {
            "nir": image.select("B5"),
            "red": image.select("B4"),
            "green": image.select("B3"),
        },
    )
    return image.addBands(mcari.rename("mcari"))


def add_mndwi(image):
    """
    Compute Modified Normalized Difference Water Index (MNDWI) using the formula:

    MNDWI = (B3 - B11) / (B3 + B11)

    Where:
    B3 = G (Green Band)
    B11 = SWIR (Shortwave Infrared Band)
    """
    mndwi = image.expression(
        "(green - swir) / (green + swir)",
        {
            "green": image.select("B3"),
            "swir": image.select("B11"),
        },
    )
    return image.addBands(mndwi.rename("mndwi"))


def add_msavi2(image):
    """
    Compute Modified Soil-Adjusted Vegetation Index 2 (MSAVI2) using the formula:

    MSAVI2 = (2 * B8 + 1 - sqrt((2 * B8 + 1)^2 - 8 * (B8 - B4))) / 2

    Where:
    B8 = NIR (Near-Infrared Band)
    B4 = R (Red Band)
    """
    msavi2 = image.expression(
        "(2 * nir + 1 - sqrt((2 * nir + 1) * (2 * nir + 1) - 8 * (nir - red))) / 2",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
        },
    )
    return image.addBands(msavi2.rename("msavi2"))


def add_mtci(image):
    """
    Compute MTCI (Meris Terrestrial Chlorophyll Index) using the formula:

    MTCI = (B6 - B5) / (B5 - B4)

    Where:
    B6 = SWIR (Shortwave Infrared Band)
    B5 = NIR (Near-Infrared Band)
    B4 = R (Red Band)
    """
    mtci = image.expression(
        "(swir - nir) / (nir - red)",
        {
            "swir": image.select("B6"),
            "nir": image.select("B5"),
            "red": image.select("B4"),
        },
    )
    return image.addBands(mtci.rename("mtci"))


def add_dni45(image):
    """
    Compute DNI45 (Drought Normalized Index 45) using the formula:

    DNI45 = (B5 - B4) / (B5 + B4)

    Where:
    B5 = NIR (Near-Infrared Band)
    B4 = R (Red Band)
    """
    dni45 = image.expression(
        "(nir - red) / (nir + red)",
        {
            "nir": image.select("B5"),
            "red": image.select("B4"),
        },
    )
    return image.addBands(dni45.rename("dni45"))


def add_ndpi(image):
    """
    Compute NDPI (Normalized Difference Plant Index) using the formula:

    NDPI = (B11 - B3) / (B11 + B3)

    Where:
    B11 = SWIR (Shortwave Infrared Band)
    B3 = G (Green Band)
    """
    ndpi = image.expression(
        "(swir - green) / (swir + green)",
        {
            "swir": image.select("B11"),
            "green": image.select("B3"),
        },
    )
    return image.addBands(ndpi.rename("ndpi"))


def add_ndti(image):
    """
    Compute NDTI (Normalized Difference Tillage Index) using the formula:

    NDTI = (B4 - B3) / (B4 + B3)

    Where:
    B4 = R (Red Band)
    B3 = G (Green Band)
    """
    ndti = image.expression(
        "(red - green) / (red + green)",
        {
            "red": image.select("B4"),
            "green": image.select("B3"),
        },
    )
    return image.addBands(ndti.rename("ndti"))


def add_ndwi(image):
    """
    Compute NDWI (Normalized Difference Water Index) using the formula:

    NDWI = (B8 - B11) / (B8 + B11)

    Where:
    B8 = NIR (Near-Infrared Band)
    B11 = SWIR (Shortwave Infrared Band)
    """
    ndwi = image.expression(
        "(nir - swir) / (nir + swir)",
        {
            "nir": image.select("B8"),
            "swir": image.select("B11"),
        },
    )
    return image.addBands(ndwi.rename("ndwi"))


def add_ndwi2(image):
    """
    Compute NDWI2 (Normalized Difference Water Index 2) using the formula:

    NDWI2 = (B3 - B8) / (B3 + B8)

    Where:
    B3 = G (Green Band)
    B8 = NIR (Near-Infrared Band)
    """
    ndwi2 = image.expression(
        "(green - nir) / (green + nir)",
        {
            "green": image.select("B3"),
            "nir": image.select("B8"),
        },
    )
    return image.addBands(ndwi2.rename("ndwi2"))


def add_pssra(image):
    """
    Compute PSSRa (Plant Stress Severity Ratio a) using the formula:

    PSSRa = B7 / B4

    Where:
    B7 = Red Edge (RE) Band
    B4 = R (Red Band)
    """
    pssra = image.expression(
        "re / red",
        {
            "re": image.select("B7"),
            "red": image.select("B4"),
        },
    )
    return image.addBands(pssra.rename("pssra"))


def add_reip(image):
    """
    Compute Sentinel 2 REIP (Red Edge Inflection Point) using the formula:

    REIP = 705 + 35 * (((B4 + B7) / 2) - B5) / (B6 - B5)

    Where:
    B4 = R (Red Band)
    B7 = Red Edge Band
    B5 = SWIR (Shortwave Infrared Band)
    B6 = NIR (Near-Infrared Band)
    """
    reip = image.expression(
        "705 + 35 * (((red + red_edge) / 2) - swir) / (nir - swir)",
        {
            "red": image.select("B4"),
            "red_edge": image.select("B7"),
            "swir": image.select("B5"),
            "nir": image.select("B6"),
        },
    )
    return image.addBands(reip.rename("reip"))


def add_ri(image):
    """
    Compute RI (Ratio Index) using the formula:

    RI = (B4^2) / (B3^3)

    Where:
    B4 = R (Red Band)
    B3 = G (Green Band)
    """
    ri = image.expression(
        "(red * red) / (green * green * green)",
        {
            "red": image.select("B4"),
            "green": image.select("B3"),
        },
    )
    return image.addBands(ri.rename("ri"))


def add_ndvi(image):
    """
    Compute NDVI (Normalized Difference Vegetation Index) using the formula:

    NDVI = (B8 - B4) / (B8 + B4)

    Where:
    B8 = NIR (Near-Infrared Band)
    B4 = R (Red Band)
    """
    ndvi = image.expression(
        "(nir - red) / (nir + red)",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
        },
    )
    return image.addBands(ndvi.rename("ndvi"))


def add_savi(image):
    """
    Compute SAVI (Soil-Adjusted Vegetation Index) using the formula:

    SAVI = (1 + L) * ((B8 - B4) / (B8 + B4 + L))

    Where:
    B8 = NIR (Near-Infrared Band)
    B4 = R (Red Band)
    L = Soil adjustment factor (set to 0.5)
    """
    L = 0.5
    savi = image.expression(
        "(1 + L) * ((nir - red) / (nir + red + L))",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
            "L": L,
        },
    )
    return image.addBands(savi.rename("savi"))


def add_tndvi(image):
    """
    Compute TNDVI (Transformed Normalized Difference Vegetation Index) using the formula:

    TNDVI = sqrt((B8 - B4) / (B8 + B4) + 0.5)

    Where:
    B8 = NIR (Near-Infrared Band)
    B4 = R (Red Band)
    """
    tndvi = image.expression(
        "sqrt((nir - red) / (nir + red) + 0.5)",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
        },
    )
    return image.addBands(tndvi.rename("tndvi"))


def add_vi(image):
    """
    Compute Vegetation Index (VI) using the formula:

    VI = B8 / B4

    Where:
    B8 = NIR (Near-Infrared Band)
    B4 = R (Red Band)
    """
    vi = image.expression(
        "nir / red",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
        },
    )
    return image.addBands(vi.rename("vi"))
