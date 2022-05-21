#!/usr/bin/env python3

# NAME TO SPECTRUM GENERATOR
# 2022 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

"""
#####################################################
##                                                 ##
##            -- STREAMLIT MAIN APP --             ##
##                                                 ##
#####################################################
"""

import string
import streamlit as st
from matplotlib import pyplot as plt
import ms2pip.single_prediction
import spectrum_utils.spectrum as spectrum
import spectrum_utils.plot as spectrum_plot

# get closest sounding letter to given letter
def get_closest_letter(letter, previous_letter):

    if letter == "B":
        return "P"
    if letter == "J":
        return "I"

    if letter in ["O", "U"]:
        if previous_letter not in ["O", "U"]:
            return "EW"
        else:
            return ""

    if letter == "X":
        return "KS"
    if letter == "Y":
        return "I"

    return ""

# preprocess name to valid amino acid shortcodes
def preprocess_name(name, impute = False):

    preprocessed_name = ""
    previous_letter = ""

    for letter in name.upper():
        if letter in ["B", "J", "O", "U", "X", "Z"]:
            if impute:
                preprocessed_name += get_closest_letter(letter, previous_letter)
        else:
            if letter in list(string.ascii_uppercase):
                preprocessed_name += letter
        previous_letter = letter

    return preprocessed_name

# predict spectrum from sequence of amino acid shortcodes
def predict_spectrum(preprocessed_name, charge = 1):

    model = ms2pip.single_prediction.SinglePrediction()
    mz, intensity, annotation = model.predict(preprocessed_name, "-", charge, model = "HCD2021")
    identifier = f"{preprocessed_name}/{charge}/-"
    precursor_mz = model.mod_info.calc_precursor_mz(preprocessed_name, "-", charge)
    mod_dict = model._modifications_to_dict("-")
    spectrum_annotation = model._get_sus_annotation(mz, annotation)

    s = spectrum.MsmsSpectrum(identifier,
                              precursor_mz,
                              charge,
                              mz,
                              intensity,
                              annotation = spectrum_annotation,
                              peptide = preprocessed_name,
                              modifications = mod_dict)

    fig = plt.figure(figsize=(16,9))
    plt.title(preprocessed_name)
    spectrum_plot.spectrum(s)
    plt.show()

    return fig

# main page content
def main_page():

    title = st.title("Name to Spectrum Generator")

    col_1, col_2 = st.columns((7, 1))

    with col_1:
        name = st.text_input("Enter your Name:", "Aletheia", help = "Enter a name, word, sentence or any valid alphabetic string to generate a corresponding spectrum.")

    with col_2:
        charge = st.selectbox("Charge:", ("1", "2", "3", "4", "5", "6"), help = "Charge of the given 'peptide'.")

    impute = st.checkbox("Impute missing letters:", value = False, help = "If letters that don't represent amino acids should be replaced by closest sounding letters.")

    if st.button("Generate Spectrum!", help = "Generate spectrum with the given input."):
        plot = st.pyplot(predict_spectrum(preprocess_name(name, impute), charge = int(charge)))

# side bar and main page loader
def main():

    about_str = \
    """
    **Name to Spectrum Generator**

    A small tool to generate mass spectra from names, words, sentences or any alphabetic strings. Uses [MS2PIP](https://github.com/compomics/ms2pip_c) for spectrum prediction.

    **Contact:** [Micha Birklbauer](mailto:micha.birklbauer@gmail.com)

    **GitHub:** [github.com/michabirklbauer/name-to-spectrum](https://github.com/michabirklbauer/name-to-spectrum/)
    """

    st.set_page_config(page_title = "Name to Spectrum Generator",
                       page_icon = ":test_tube:",
                       layout = "centered",
                       initial_sidebar_state = "expanded",
                       menu_items = {"Get Help": "https://github.com/michabirklbauer/name-to-spectrum/discussions",
                                     "Report a bug": "https://github.com/michabirklbauer/name-to-spectrum/issues",
                                     "About": about_str}
                       )

    title = st.sidebar.title("Name to Spectrum Generator")

    logo = st.sidebar.image("img/fhooe_logo.png", caption = "Presented by the Bioinformatics Research Group of the University of Applied Sciences Upper Austria, Hagenberg.")

    doc = st.sidebar.markdown("A small tool to generate mass spectra from names, words, sentences or any alphabetic strings.")

    socials_str = \
        """
        **More About Us:**

        **Bioinformatics Research Group Hagenberg:**  """ + """
        [Who we are](https://bioinformatics.fh-hagenberg.at/bin_typo3/htdocs/index.php?id=home)

        **Study Bioinformatics in Hagenberg:**  """ + """
        [Study MBI](https://www.fh-ooe.at/campus-hagenberg/studiengaenge/bachelor/medizin-und-bioinformatik/)

        **Study Data Science and Engineering in Hagenberg:**  """ + """
        [Study DSE](https://www.fh-ooe.at/campus-hagenberg/studiengaenge/master/data-science-und-engineering/)
        """
    socials = st.sidebar.markdown(socials_str)

    main_page()

if __name__ == "__main__":
    main()
