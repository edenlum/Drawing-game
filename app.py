import streamlit as st
import streamlit.components.v1 as components
import uuid
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Drawing Pad",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .sidebar .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
    .stButton > button {
        width: 100%;
        background-color: #2E86AB;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #1f5f7a;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_color' not in st.session_state:
    st.session_state.selected_color = "#000000"
if 'selected_brush_size' not in st.session_state:
    st.session_state.selected_brush_size = 5
if 'current_page' not in st.session_state:
    st.session_state.current_page = "lobby"
if 'game_id' not in st.session_state:
    st.session_state.game_id = None
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""
if 'is_host' not in st.session_state:
    st.session_state.is_host = False
if 'games' not in st.session_state:
    st.session_state.games = {}
if 'current_game' not in st.session_state:
    st.session_state.current_game = None

def generate_game_id():
    """Generate a unique 6-character game ID"""
    return str(uuid.uuid4())[:6].upper()

def create_game(player_name):
    """Create a new game and return game ID"""
    game_id = generate_game_id()
    game_data = {
        'id': game_id,
        'host': player_name,
        'players': [player_name],
        'created_at': datetime.now(),
        'status': 'waiting',  # waiting, playing, finished
        'canvas_data': None,
        'current_drawer': None,
        'round': 1,
        'max_rounds': 3
    }
    st.session_state.games[game_id] = game_data
    return game_id

def join_game(game_id, player_name):
    """Join an existing game"""
    if game_id in st.session_state.games:
        if player_name not in st.session_state.games[game_id]['players']:
            st.session_state.games[game_id]['players'].append(player_name)
        return True
    return False

def get_game_info(game_id):
    """Get information about a specific game"""
    return st.session_state.games.get(game_id, None)

def cleanup_old_games():
    """Remove games older than 1 hour"""
    current_time = datetime.now()
    games_to_remove = []
    for game_id, game_data in st.session_state.games.items():
        if current_time - game_data['created_at'] > timedelta(hours=1):
            games_to_remove.append(game_id)
    
    for game_id in games_to_remove:
        del st.session_state.games[game_id]

def lobby_page():
    """Display the lobby page for creating and joining games"""
    st.markdown('<h1 class="main-header">🎨 Drawing Game Lobby</h1>', unsafe_allow_html=True)
    
    # Clean up old games
    cleanup_old_games()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎮 Create New Game")
        st.markdown("Start a new drawing game and invite friends!")
        
        player_name = st.text_input("Your Name", value=st.session_state.player_name, key="create_name")
        
        if st.button("🚀 Create Game", type="primary", use_container_width=True):
            if player_name.strip():
                st.session_state.player_name = player_name.strip()
                game_id = create_game(player_name.strip())
                st.session_state.game_id = game_id
                st.session_state.is_host = True
                st.session_state.current_page = "game"
                st.rerun()
            else:
                st.error("Please enter your name!")
    
    with col2:
        st.subheader("🔗 Join Existing Game")
        st.markdown("Enter a game ID to join an existing game!")
        
        join_name = st.text_input("Your Name", value=st.session_state.player_name, key="join_name")
        game_id_input = st.text_input("Game ID", placeholder="Enter 6-character game ID", max_chars=6)
        
        if st.button("🎯 Join Game", type="secondary", use_container_width=True):
            if join_name.strip() and game_id_input.strip():
                st.session_state.player_name = join_name.strip()
                if join_game(game_id_input.strip().upper(), join_name.strip()):
                    st.session_state.game_id = game_id_input.strip().upper()
                    st.session_state.is_host = False
                    st.session_state.current_page = "game"
                    st.rerun()
                else:
                    st.error("Game not found! Please check the Game ID.")
            else:
                st.error("Please enter both your name and game ID!")
    
    # Display active games
    st.subheader("🏠 Active Games")
    if st.session_state.games:
        for game_id, game_data in st.session_state.games.items():
            with st.expander(f"Game {game_id} - {len(game_data['players'])} players"):
                st.write(f"**Host:** {game_data['host']}")
                st.write(f"**Players:** {', '.join(game_data['players'])}")
                st.write(f"**Status:** {game_data['status'].title()}")
                st.write(f"**Created:** {game_data['created_at'].strftime('%H:%M:%S')}")
                
                if st.button(f"Join Game {game_id}", key=f"join_{game_id}"):
                    if st.session_state.player_name:
                        if join_game(game_id, st.session_state.player_name):
                            st.session_state.game_id = game_id
                            st.session_state.is_host = False
                            st.session_state.current_page = "game"
                            st.rerun()
                        else:
                            st.error("Failed to join game!")
                    else:
                        st.error("Please enter your name first!")
    else:
        st.info("No active games. Create one to get started!")
    
    # Instructions
    with st.expander("📖 How to Play"):
        st.markdown("""
        **Getting Started:**
        1. **Create a Game**: Enter your name and click "Create Game" to get a unique Game ID
        2. **Share Game ID**: Share the 6-character Game ID with friends
        3. **Join Game**: Friends can enter the Game ID to join your game
        4. **Start Drawing**: Once everyone joins, the host can start the game
        
        **Game Rules:**
        - Players take turns drawing
        - Others guess what's being drawn
        - Points are awarded for correct guesses
        - The player with the most points wins!
        """)

def game_page():
    """Display the main game page"""
    if not st.session_state.game_id or st.session_state.game_id not in st.session_state.games:
        st.error("Game not found! Returning to lobby.")
        st.session_state.current_page = "lobby"
        st.rerun()
        return
    
    game_data = st.session_state.games[st.session_state.game_id]
    
    # Game header
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### 🎮 Game {st.session_state.game_id}")
    
    with col2:
        if st.button("🏠 Back to Lobby"):
            st.session_state.current_page = "lobby"
            st.rerun()
    
    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Game info
    st.info(f"**Players:** {', '.join(game_data['players'])} | **Status:** {game_data['status'].title()} | **Round:** {game_data['round']}/{game_data['max_rounds']}")
    
    # Host controls
    if st.session_state.is_host:
        st.subheader("🎛️ Host Controls")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ Start Game", type="primary"):
                st.session_state.games[st.session_state.game_id]['status'] = 'playing'
                st.rerun()
        
        with col2:
            if st.button("⏸️ Pause Game"):
                st.session_state.games[st.session_state.game_id]['status'] = 'waiting'
                st.rerun()
        
        with col3:
            if st.button("🛑 End Game"):
                st.session_state.games[st.session_state.game_id]['status'] = 'finished'
                st.rerun()
    
    # Drawing area
    if game_data['status'] == 'playing':
        st.subheader("🎨 Drawing Canvas")
        
        # Sidebar controls
        with st.sidebar:
            st.header("🎛️ Drawing Controls")
            
            # Canvas size
            st.subheader("Canvas Size")
            width = st.slider("Width", 400, 1200, 800, 50)
            height = st.slider("Height", 300, 800, 600, 50)
            
            # Drawing tools
            st.subheader("Drawing Tools")
            brush_size = st.slider("Brush Size", 1, 20, 5)
            
            # Color picker
            color = st.color_picker("Choose Color", "#000000")
            
            # Tool selection
            tool = st.selectbox("Tool", ["Brush", "Eraser"])
            
            # Instructions
            st.subheader("📝 Instructions")
            st.info("""
            **How to draw:**
            1. Click and drag on the canvas to draw
            2. Use the controls above to adjust settings
            3. Switch between Brush and Eraser tools
            4. Clear or download your artwork
            """)
        
        # Create and display the drawing canvas
        canvas_html = create_drawing_canvas(width, height, brush_size, color, tool)
        components.html(canvas_html, height=height + 100)
        
        # Game chat/guessing area
        st.subheader("💬 Game Chat")
        st.text_input("Type your guess here...", key="guess_input")
        
        if st.button("Send Guess"):
            st.success("Guess sent!")
    
    elif game_data['status'] == 'waiting':
        st.subheader("⏳ Waiting for Host to Start Game")
        st.info("The host will start the game when everyone is ready!")
        
        # Show player list
        st.write("**Players in this game:**")
        for i, player in enumerate(game_data['players'], 1):
            st.write(f"{i}. {player}")
    
    elif game_data['status'] == 'finished':
        st.subheader("🏁 Game Finished!")
        st.success("Thanks for playing! The host can start a new game or you can return to the lobby.")

def create_drawing_canvas(width, height, brush_size, color, tool):
    """Create HTML canvas with drawing functionality"""
    canvas_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
            }}
            #drawingCanvas {{
                border: 2px solid #ddd;
                border-radius: 8px;
                cursor: crosshair;
                background-color: white;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .controls {{
                margin-bottom: 10px;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }}
            .control-group {{
                display: inline-block;
                margin-right: 20px;
            }}
            label {{
                font-weight: bold;
                margin-right: 5px;
            }}
            input, select {{
                margin-right: 10px;
            }}
            button {{
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                margin-right: 10px;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="controls">
            <div class="control-group">
                <label>Brush Size:</label>
                <input type="range" id="brushSize" min="1" max="20" value="{brush_size}">
                <span id="brushSizeValue">{brush_size}</span>
            </div>
            <div class="control-group">
                <label>Color:</label>
                <input type="color" id="colorPicker" value="{color}">
            </div>
            <div class="control-group">
                <label>Tool:</label>
                <select id="toolSelect">
                    <option value="brush" {'selected' if tool == 'Brush' else ''}>Brush</option>
                    <option value="eraser" {'selected' if tool == 'Eraser' else ''}>Eraser</option>
                </select>
            </div>
            <button onclick="clearCanvas()">Clear Canvas</button>
            <button onclick="downloadCanvas()">Download</button>
        </div>
        
        <canvas id="drawingCanvas" width="{width}" height="{height}"></canvas>
        
        <script>
            const canvas = document.getElementById('drawingCanvas');
            const ctx = canvas.getContext('2d');
            const brushSizeSlider = document.getElementById('brushSize');
            const brushSizeValue = document.getElementById('brushSizeValue');
            const colorPicker = document.getElementById('colorPicker');
            const toolSelect = document.getElementById('toolSelect');
            
            let isDrawing = false;
            let lastX = 0;
            let lastY = 0;
            
            // Set initial canvas background
            ctx.fillStyle = 'white';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Update brush size display
            brushSizeSlider.addEventListener('input', function() {{
                brushSizeValue.textContent = this.value;
            }});
            
            // Mouse events
            canvas.addEventListener('mousedown', startDrawing);
            canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('mouseup', stopDrawing);
            canvas.addEventListener('mouseout', stopDrawing);
            
            // Touch events for mobile
            canvas.addEventListener('touchstart', handleTouch);
            canvas.addEventListener('touchmove', handleTouch);
            canvas.addEventListener('touchend', stopDrawing);
            
            function startDrawing(e) {{
                isDrawing = true;
                const rect = canvas.getBoundingClientRect();
                lastX = e.clientX - rect.left;
                lastY = e.clientY - rect.top;
            }}
            
            function draw(e) {{
                if (!isDrawing) return;
                
                const rect = canvas.getBoundingClientRect();
                const currentX = e.clientX - rect.left;
                const currentY = e.clientY - rect.top;
                
                ctx.beginPath();
                ctx.moveTo(lastX, lastY);
                ctx.lineTo(currentX, currentY);
                
                if (toolSelect.value === 'eraser') {{
                    ctx.globalCompositeOperation = 'destination-out';
                    ctx.lineWidth = brushSizeSlider.value * 2;
                }} else {{
                    ctx.globalCompositeOperation = 'source-over';
                    ctx.strokeStyle = colorPicker.value;
                    ctx.lineWidth = brushSizeSlider.value;
                }}
                
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.stroke();
                
                lastX = currentX;
                lastY = currentY;
            }}
            
            function stopDrawing() {{
                isDrawing = false;
            }}
            
            function handleTouch(e) {{
                e.preventDefault();
                const touch = e.touches[0];
                const mouseEvent = new MouseEvent(e.type === 'touchstart' ? 'mousedown' : 
                                                e.type === 'touchmove' ? 'mousemove' : 'mouseup', {{
                    clientX: touch.clientX,
                    clientY: touch.clientY
                }});
                canvas.dispatchEvent(mouseEvent);
            }}
            
            function clearCanvas() {{
                ctx.fillStyle = 'white';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }}
            
            function downloadCanvas() {{
                const link = document.createElement('a');
                link.download = 'drawing.png';
                link.href = canvas.toDataURL();
                link.click();
            }}
        </script>
    </body>
    </html>
    """
    return canvas_html

def main():
    """Main application function with page routing"""
    # Page routing
    if st.session_state.current_page == "lobby":
        lobby_page()
    elif st.session_state.current_page == "game":
        game_page()
    else:
        # Default to lobby
        st.session_state.current_page = "lobby"
        lobby_page()

if __name__ == "__main__":
    main()
