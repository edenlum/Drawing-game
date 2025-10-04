# 🎨 Drawing Pad

A beautiful and interactive drawing pad application built with Streamlit. Create digital artwork with customizable brushes, colors, and canvas sizes.

## Features

- 🖌️ **Customizable Drawing Tools**: Adjustable brush sizes and colors
- 🎨 **Color Picker**: Choose from millions of colors or use quick preset colors
- 📏 **Flexible Canvas**: Resize your canvas from 400x300 to 1200x800 pixels
- 🗑️ **Clear Function**: Start fresh anytime with the clear canvas button
- 💾 **Download**: Save your artwork as PNG files
- 🎯 **Eraser Tool**: Fix mistakes with the built-in eraser
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd Drawing-game
   ```

2. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## Usage

### Getting Started
1. Launch the application using `streamlit run app.py`
2. Use the sidebar controls to customize your drawing experience
3. Start drawing by clicking and dragging on the canvas

### Drawing Controls
- **Brush Size**: Adjust the thickness of your brush (1-20 pixels)
- **Color Picker**: Choose any color for your brush
- **Quick Colors**: Use preset colors for faster access
- **Tool Selection**: Switch between Brush and Eraser modes
- **Canvas Size**: Resize your drawing area as needed

### Saving Your Work
- Click the "Download Drawing" button to save your artwork as a PNG file
- Use the "Clear Canvas" button to start a new drawing

## Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pillow (PIL)**: Image processing and manipulation
- **NumPy**: Numerical operations
- **OpenCV**: Computer vision library (for potential future enhancements)

### File Structure
```
Drawing-game/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── LICENSE            # License file
```

## Customization

You can easily customize the application by modifying `app.py`:

- **Colors**: Change the color scheme in the CSS section
- **Canvas Sizes**: Adjust the minimum and maximum canvas dimensions
- **Brush Sizes**: Modify the available brush size options
- **UI Elements**: Add new controls or modify existing ones

## Troubleshooting

### Common Issues

1. **Port already in use**: If port 8501 is busy, Streamlit will automatically use the next available port
2. **Missing dependencies**: Make sure all packages in `requirements.txt` are installed
3. **Drawing not working**: This is a limitation of Streamlit's current drawing capabilities. The app provides a foundation that can be enhanced with additional libraries

### Performance Tips
- Use smaller canvas sizes for better performance
- Clear the canvas regularly to free up memory
- Close other browser tabs to improve responsiveness

## Future Enhancements

Potential improvements for future versions:
- Real-time drawing with mouse/touch events
- Layer support for complex drawings
- Shape tools (rectangles, circles, lines)
- Text tool for adding labels
- Undo/redo functionality
- Drawing history and version control
- Collaborative drawing features

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Inspired by digital art and drawing applications
- Thanks to the open-source community for the amazing tools and libraries
