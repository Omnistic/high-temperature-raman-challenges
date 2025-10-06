import numpy as np
import plotly.graph_objects as go
from scipy.constants import pi, speed_of_light, Boltzmann, Planck

def blackbody_radiation(wavelength, temperature_k):
    intensity = 2*pi*Planck*speed_of_light**2 / wavelength**5
    intensity /= np.exp(Planck*speed_of_light / (wavelength*Boltzmann*temperature_k)) - 1
    return intensity

temperature_k = np.arange(1500, 3001, 500)
wavelength_nm = np.linspace(350, 800, 100)
wavelength = wavelength_nm * 1e-9

blackbody_spectra = []
for tt in temperature_k:
    blackbody_spectra.append(blackbody_radiation(wavelength, tt) * 1e-6)

laser_wavelength_nm = [405, 532]
raman_shift_per_cm = 4000
raman_shift_nm = [(1/wl - raman_shift_per_cm/1e7)**-1 for wl in laser_wavelength_nm]

y_max = np.max(blackbody_spectra)
y_max += y_max * 0.1

fillcols = ['Gray', 'LightGray']

fig = go.Figure()
for ii, wl in enumerate(laser_wavelength_nm):
    fig.add_shape(
        type='rect',
        x0=wl, x1=raman_shift_nm[ii],
        y0=0, y1=y_max,
        fillcolor=fillcols[ii]
    )
    fig.add_vline(
        x=wl,
        line=dict(
            color='Black',
            dash='dash',
            width=2
        ),
        annotation_text=f'Laser {wl} nm<BR>+ {raman_shift_per_cm} cm⁻¹',
        annotation_position='top right'
    )
for ii, blackbody_spectrum in enumerate(blackbody_spectra):
    fig.add_trace(go.Scatter(
        x=wavelength_nm,
        y=blackbody_spectrum,
        mode='lines',
        name=f'{temperature_k[ii]:d} K'
    ))
fig.update_xaxes(
    title_text='Wavelength (nm)',
    showgrid=True
)
fig.update_yaxes(
    title_text='Spectral irradiance (Wm⁻²µm⁻¹)',
)
fig.update_layout(
    template='simple_white'
)
fig.show()
fig.write_image('high_temperature_raman.png')