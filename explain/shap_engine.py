import shap
import matplotlib.pyplot as plt

plt.switch_backend('Agg')


def generate_shap_plot(shap_values):

    shap.plots.waterfall(shap_values[0], show=False)

    plt.savefig(
        "static/shap/shap_plot.png",
        bbox_inches='tight'
    )

    plt.close()