import gradio as gr

theme = gr.themes.Default(
    primary_hue="blue",
    secondary_hue="purple",
    font=[gr.themes.GoogleFont('proxima-nova'), 'ui-sans-serif', 'system-ui', 'sans-serif'],
).set(
    border_color_accent_subdued='*border_color_accent',
    checkbox_label_background_fill='*button_secondary_background_fill',
    checkbox_label_background_fill_dark='*button_secondary_background_fill',
    checkbox_label_background_fill_hover='*button_secondary_background_fill_hover',
    checkbox_label_background_fill_hover_dark='*button_secondary_background_fill_hover',
    error_background_fill_dark='*background_fill_primary',
    input_background_fill='*neutral_100',
    input_background_fill_dark='*neutral_700',
    input_border_width='0px',
    input_border_width_dark='0px',
    input_shadow_focus='*input_shadow',
    input_shadow_focus_dark='*input_shadow',
    stat_background_fill='*primary_300',
    stat_background_fill_dark='*primary_500',
    button_border_width='*input_border_width',
    button_border_width_dark='*input_border_width',
    button_cancel_background_fill='*button_secondary_background_fill',
    button_cancel_background_fill_dark='*button_secondary_background_fill',
    button_cancel_background_fill_hover='*button_secondary_background_fill_hover',
    button_cancel_background_fill_hover_dark='*button_secondary_background_fill_hover',
    button_cancel_text_color='*button_secondary_text_color',
    button_cancel_text_color_dark='*button_secondary_text_color',
    button_cancel_text_color_hover='*button_secondary_text_color_hover'
)
