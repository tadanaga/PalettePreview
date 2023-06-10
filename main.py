import streamlit as st
import seaborn as sns

# remove hamburger & footer
st.markdown("""
<style>
.css-14xtw13.e13qjvis0
{
   visibility: hidden;
}
.css-cio0dv.e1g8pov61
{
   visibility: hidden;
}
</style>
""",unsafe_allow_html=True)

palettes = ['deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind', 'rocket',
   'mako', 'flare', 'crest', 'vlag', 'icefire', 'viridis', 'plasma', 'inferno', 'magma',
   'cividis', 'twilight', 'twilight_shifted', 'hsv', 'husl']

# Available color palettes
PALETTES = {
    'Standard': ['bright', 'colorblind', 'dark', 'deep', 'muted', 'pastel'],
    'Categorical': ['Accent', 'Set1', 'Set2', 'Set3', 'hsl','Pastel1', 'Pastel2','tab10', 'tab20', 'tab20b', 'tab20c'],
    'Sequential': ['cividis', 'inferno', 'magma', 'mako', 'plasma', 'rocket', 'viridis'],
    'Diverging': ['bwr', 'coolwarm', 'icefire', 'PuOr', 'RdYlBu', 'RdYlGn', 'seismic', 'Spectral', 'vlag'],
    'Monochrome': ['Blues', 'Greens', 'Oranges', 'Purples', 'Reds'],
    'Pair': ['Paired'],
    # Add more categories and palettes as needed
}

# Color code formats
color_formats = ['rgb', 'RGB', 'HTML']

# Syntax options
syntax_options = ['Matlab', 'Python', 'LaTeX']

def generate_colors(num_colors, palette):
   colors = sns.color_palette(palette, num_colors)
   return colors

def format_color_code(color, code_format):
   if code_format == 'rgb':
      return f"{color[0]:.6f},{color[1]:.6f},{color[2]:.6f}"
   elif code_format == 'RGB':
      return f"{int(color[0] * 255)},{int(color[1] * 255)},{int(color[2] * 255)}"
   elif code_format == 'HTML':
      hex_code = '#'
      for channel in color:
         hex_code += f"{int(channel * 255):02x}"
      return hex_code

def generate_color_code(colors, code_format, syntax):
   color_code = ""
   if syntax == 'Matlab':
      color_code += 'colors = ['
      for color in colors:
         if code_format=="HTML":
            color_code += f"\"{format_color_code(color,code_format)}\","
         else:
            color_code += f"{format_color_code(color,code_format)};"
      if code_format=="HTML":
         color_code = color_code.rstrip(',')
      else:
         color_code = color_code.rstrip(';')
      color_code += '];'
   elif syntax == 'Python':
      if code_format=="HTML":
         color_code += 'colors = ['
         for color in colors:
            color_code += f"\"{format_color_code(color, code_format)}\","
         color_code = color_code.rstrip(',')
         color_code +="]"
      else:
         color_code += 'colors = np.array(['
         for color in colors:
            color_code += f"[{format_color_code(color, code_format)}], "
         color_code = color_code.rstrip(', ')
         color_code += '])'
   elif syntax == 'LaTeX':
      color_code += ''
      count=0
      for color in colors:
         color_code += f"\\definecolor{{c{count:02d}}}{{{code_format}}}{{{format_color_code(color, code_format)}}}\n"
         count+=1
      color_code = color_code.rstrip(', ')
   return color_code

# Streamlit app
def main():
   st.title("Palette Preview")
   st.write("This is a tool to preview Seaborn color palettes and obtain the code for a discrete set of colors.")

   st.header("Choose the parameters")
   palette_category = st.radio("Palette Category", list(PALETTES.keys()))
   palette = st.selectbox("Palette", PALETTES[palette_category])
   num_colors = st.slider("Number of Colors", 1, 20, 5)
   # palette = st.selectbox("Seaborn Color Palette", palettes)
   code_format = st.selectbox("Color Code Format", color_formats)
   syntax = st.selectbox("Language", syntax_options)
   colors = generate_colors(num_colors, palette)

   st.subheader("Colors")

   # Display colors as squares side-by-side
   row_size = 10  # Number of squares per row
   col_size = num_colors // row_size
   for i in range(col_size + 1):
      col_colors = colors[i * row_size : (i + 1) * row_size]
      col_squares = ""
      for color in col_colors:
         col_squares += f'<div style="background-color: rgb({int(color[0] * 255)}, {int(color[1] * 255)}, {int(color[2] * 255)})'
         col_squares += '; width: 50px; height: 50px; display: inline-block; margin: 5px"></div>'
      st.markdown(col_squares, unsafe_allow_html=True)

   color_code = generate_color_code(colors, code_format, syntax)

   st.subheader("Code")
   st.code(color_code)


if __name__ == "__main__":
   main()
