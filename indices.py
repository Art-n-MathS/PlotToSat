### Version 1. Author Dr Finely Gibson 2024-2025 

# sentinel2_indices.py

INDEX_NAMES = [
    "arvi",
    "bi",
    "bi2",
    "ci",
    "dvi",
    "gemi",
    "gndvi",
    "ipvi",
    "ireci",
    "mcari",
    "mndwi",
    "msavi",
    "msavi2",
    "mtci",
    "ndi45",
    "ndpi",
    "ndti",
    "ndvi",
    "ndwi",
    "ndwi2",
    "pssra",
    "pvi",
    "reip",
    "ri",
    "rvi",
    "s2rep",
    "savi",
    "tndvi",
    "tsavi",
    "wdvi",
]


def add_ndvi(image):
    # NDVI = (NIR - Red) / (NIR + Red)
    ndvi = image.expression(
        "(nir - red) / (nir + red)",
        {"nir": image.select("B8"), "red": image.select("B4")},
    )
    return image.addBands(ndvi.rename("ndvi"))


def add_dvi(image):
    # DVI = NIR - Red
    dvi = image.expression(
        "nir - red",
        {"nir": image.select("B8"), "red": image.select("B4")},
    )
    return image.addBands(dvi.rename("dvi"))


def add_rvi(image):
    # RVI = NIR / Red
    rvi = image.expression(
        "nir / red",
        {"nir": image.select("B8"), "red": image.select("B4")},
    )
    return image.addBands(rvi.rename("rvi"))


def add_pvi(image):
    # PVI = (NIR - a * Red) / (sqrt(a^2 + 1))
    a = 0.1  # Slope value, adjust as needed
    pvi = image.expression(
        "(nir - a * red) / (sqrt(a * a + 1))",
        {"nir": image.select("B8"), "red": image.select("B4"), "a": a},
    )
    return image.addBands(pvi.rename("pvi"))


def add_ipvi(image):
    # IPVI = (NIR - Red) / (NIR + Red + Green)
    ipvi = image.expression(
        "(nir - red) / (nir + red + green)",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
            "green": image.select("B3"),
        },
    )
    return image.addBands(ipvi.rename("ipvi"))


def add_wdvi(image):
    # WDVI = NIR - (a * Red)
    a = 0.1  # Slope value, adjust as needed
    wdvi = image.expression(
        "nir - (a * red)",
        {"nir": image.select("B8"), "red": image.select("B4"), "a": a},
    )
    return image.addBands(wdvi.rename("wdvi"))


def add_tndvi(image):
    # TNDVI = (NIR - Red) / (NIR + Red + 0.08)
    tndvi = image.expression(
        "(nir - red) / (nir + red + 0.08)",
        {"nir": image.select("B8"), "red": image.select("B4")},
    )
    return image.addBands(tndvi.rename("tndvi"))


def add_gndvi(image):
    # GNDVI = (NIR - Green) / (NIR + Green)
    gndvi = image.expression(
        "(nir - green) / (nir + green)",
        {"nir": image.select("B8"), "green": image.select("B3")},
    )
    return image.addBands(gndvi.rename("gndvi"))


def add_gemi(image):
    # GEMI = (2 * (NIR^2 - Red^2) + 1.5 * NIR + 0.5 * Red) / (NIR + 0.5)
    gemi = image.expression(
        "(2 * (nir^2 - red^2) + 1.5 * nir + 0.5 * red) / (nir + 0.5)",
        {"nir": image.select("B8"), "red": image.select("B4")},
    )
    return image.addBands(gemi.rename("gemi"))


def add_arvi(image):
    # ARVI = (NIR - (2 * Red) + Blue) / (NIR + (2 * Red) + Blue)
    arvi = image.expression(
        "(nir - (2 * red) + blue) / (nir + (2 * red) + blue)",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
            "blue": image.select("B2"),
        },
    )
    return image.addBands(arvi.rename("arvi"))


def add_ndi45(image):
    # NDI45 = (NIR - Green) / (NIR + Green)
    ndi45 = image.expression(
        "(nir - green) / (nir + green)",
        {"nir": image.select("B8"), "green": image.select("B3")},
    )
    return image.addBands(ndi45.rename("ndi45"))


def add_mtci(image):
    # MTCI = (NIR - Red Edge) / (Green - Blue)
    mtci = image.expression(
        "(nir - red_edge) / (green - blue)",
        {
            "nir": image.select("B8"),
            "red_edge": image.select("B5"),
            "green": image.select("B3"),
            "blue": image.select("B2"),
        },
    )
    return image.addBands(mtci.rename("mtci"))


def add_mcari(image):
    # MCARI = ((NIR - Red) - 0.2 * (NIR - Green)) * (NIR / Red)
    mcari = image.expression(
        "((nir - red) - 0.2 * (nir - green)) * (nir / red)",
        {
            "nir": image.select("B8"),
            "red": image.select("B4"),
            "green": image.select("B3"),
        },
    )
    return image.addBands(mcari.rename("mcari"))


def add_reip(image):
    # REIP = (NIR - Red Edge) / (NIR + Red Edge)
    reip = image.expression(
        "(nir - red_edge) / (nir + red_edge)",
        {"nir": image.select("B8"), "red_edge": image.select("B5")},
    )
    return image.addBands(reip.rename("reip"))


def add_s2rep(image):
    # S2REP = (NIR - SWIR) / (NIR + SWIR)
    s2rep = image.expression(
        "(nir - swir) / (nir + swir)",
        {"nir": image.select("B8"), "swir": image.select("B11")},
    )
    return image.addBands(s2rep.rename("s2rep"))


def add_ireci(image):
    # IRECI = (Red - Green) / (Red + Green)
    ireci = image.expression(
        "(red - green) / (red + green)",
        {"red": image.select("B4"), "green": image.select("B3")},
    )
    return image.addBands(ireci.rename("ireci"))


def add_pssra(image):
    # PSSRa = (SWIR - NIR) / (SWIR + NIR)
    pssra = image.expression(
        "(swir - nir) / (swir + nir)",
        {"swir": image.select("B11"), "nir": image.select("B8")},
    )
    return image.addBands(pssra.rename("pssra"))


def add_savi(image, L=0.5):
    # SAVI = (NIR - Red) * (1 + L) / (NIR + Red + L)
    savi = image.expression(
        "(nir - red) * (1 + L) / (nir + red + L)",
        {"nir": image.select("B8"), "red": image.select("B4"), "L": L},
    )
    return image.addBands(savi.rename("savi"))


def add_tsavi(image):
    # TSAVI = (NIR - Red) / (NIR + Red + 0.2)
    tsavi = image.expression(
        "(nir - red) / (nir + red + 0.2)",
        {"nir": image.select("B8"), "red": image.select("B4")},
    )
    return image.addBands(tsavi.rename("tsavi"))


def add_msavi(image):
    # MSAVI = (2 * NIR + 1 - sqrt((2 * NIR + 1)^2 - 8 * (NIR - Red))) / 2
    msavi = image.expression(
        "(2 * nir + 1 - sqrt((2 * nir + 1) ^ 2 - 8 * (nir - red))) / 2",
        {"nir": image.select("B8"), "red": image.select("B4")},
    )
    return image.addBands(msavi.rename("msavi"))


def add_msavi2(image):
    # MSAVI2 = (2 * NIR + 1 - sqrt((2 * NIR + 1)^2 - 8 * (NIR - Red))) / 2
    msavi2 = image.expression(
        "(2 * nir + 1 - sqrt((2 * nir + 1) ^ 2 - 8 * (nir - red))) / 2",
        {"nir": image.select("B8"), "red": image.select("B4")},
    )
    return image.addBands(msavi2.rename("msavi2"))


def add_bi(image):
    # BI = (Green + Red) - NIR
    bi = image.expression(
        "(green + red) - nir",
        {
            "green": image.select("B3"),
            "red": image.select("B4"),
            "nir": image.select("B8"),
        },
    )
    return image.addBands(bi.rename("bi"))


def add_bi2(image):
    # BI2 = (Green + Red) - NIR
    bi2 = image.expression(
        "(green + red) - nir",
        {
            "green": image.select("B3"),
            "red": image.select("B4"),
            "nir": image.select("B8"),
        },
    )
    return image.addBands(bi2.rename("bi2"))


def add_ri(image):
    # RI = NIR / Red
    ri = image.expression(
        "nir / red",
        {"nir": image.select("B8"), "red": image.select("B4")},
    )
    return image.addBands(ri.rename("ri"))


def add_ci(image):
    # CI = (NIR - Red) / (NIR + Red)
    ci = image.expression(
        "(nir - red) / (nir + red)",
        {"nir": image.select("B8"), "red": image.select("B4")},
    )
    return image.addBands(ci.rename("ci"))


def add_ndwi(image):
    # NDWI = (Green - NIR) / (Green + NIR)
    ndwi = image.expression(
        "(green - nir) / (green + nir)",
        {"nir": image.select("B8"), "green": image.select("B3")},
    )
    return image.addBands(ndwi.rename("ndwi"))


def add_ndwi2(image):
    # NDWI2 = (Green - SWIR) / (Green + SWIR)
    ndwi2 = image.expression(
        "(green - swir) / (green + swir)",
        {"green": image.select("B3"), "swir": image.select("B11")},
    )
    return image.addBands(ndwi2.rename("ndwi2"))


def add_mndwi(image):
    # MNDWI = (Green - SWIR) / (Green + SWIR)
    mndwi = image.expression(
        "(green - swir) / (green + swir)",
        {"green": image.select("B3"), "swir": image.select("B11")},
    )
    return image.addBands(mndwi.rename("mndwi"))


def add_ndpi(image):
    # NDPI = (NIR - SWIR) / (NIR + SWIR)
    ndpi = image.expression(
        "(nir - swir) / (nir + swir)",
        {"nir": image.select("B8"), "swir": image.select("B11")},
    )
    return image.addBands(ndpi.rename("ndpi"))


def add_ndti(image):
    # NDTI = (SWIR - NIR) / (SWIR + NIR)
    ndti = image.expression(
        "(swir - nir) / (swir + nir)",
        {"nir": image.select("B8"), "swir": image.select("B11")},
    )
    return image.addBands(ndti.rename("ndti"))
