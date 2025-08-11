import React, { useEffect, useRef, useState, useCallback } from 'react';

const Background3D = ({ darkMode = true, theme }) => {
  // Use darkMode prop if theme is not provided, otherwise use theme
  const currentTheme = theme || (darkMode ? 'dark' : 'light');
  
  const canvasRef = useRef(null);
  const mouseRef = useRef({ x: -1000, y: -1000, radius: 150 });
  const [nodes, setNodes] = useState([]);
  const [connections, setConnections] = useState([]);
  // Refs to avoid stale state in RAF loop
  const nodesRef = useRef([]);
  const connectionsRef = useRef([]);
  const [pulseActive, setPulseActive] = useState(false);
  const [mouse, setMouse] = useState({ x: -1000, y: -1000, radius: 150 });
  const animationRef = useRef(null);

  // Define colors based on theme
  const colors = {
    dark: {
      background: { start: '#0a0a0a', end: '#000000' },
      node: 'rgba(255, 255, 255, ',
      edge: 'rgba(255, 255, 255, ',
      grid: 'rgba(255, 255, 255, 0.05)',
      mouseInfluence: { start: 'rgba(255, 255, 255, 0.15)', end: 'rgba(255, 255, 255, 0)' },
      mouseConnection: { start: 'rgba(255, 255, 255, ', end: 'rgba(255, 255, 255, ' }
    },
    light: {
      background: { start: '#f0f0f0', end: '#ffffff' },
      node: 'rgba(0, 0, 0, ',
      edge: 'rgba(0, 0, 0, ',
      grid: 'rgba(0, 0, 0, 0.05)',
      mouseInfluence: { start: 'rgba(0, 0, 0, 0.15)', end: 'rgba(0, 0, 0, 0)' },
      mouseConnection: { start: 'rgba(0, 0, 0, ', end: 'rgba(0, 0, 0, ' }
    }
  };

  const currentColors = colors[currentTheme];

  // Node class
  class Node {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      // Increased node size for better visibility
      this.size = Math.random() * 2.5 + 1.5;
      this.baseSize = this.size;
      
      // Random initial direction and speed
      const angle = Math.random() * Math.PI * 2;
      const speed = 0.2 + Math.random() * 0.3; // Slow random speed
      this.speedX = Math.cos(angle) * speed;
      this.speedY = Math.sin(angle) * speed;
      
      this.opacity = Math.random() * 0.3 + 0.7; // Higher base opacity
      this.pulsePhase = Math.random() * Math.PI * 2;
      this.activity = Math.random() * 0.5 + 0.5; // Higher base activity
      this.mouseInfluence = 0;
      
      // For random direction changes
      this.directionChangeTimer = 0;
      this.directionChangeInterval = 100 + Math.random() * 200; // Change direction every 100-300 frames
    }
    
    update(mouse, canvas) {
      // Mouse interaction
      const dx = this.x - mouse.x;
      const dy = this.y - mouse.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < mouse.radius) {
        // Calculate mouse influence (stronger when closer)
        this.mouseInfluence = 1 - (distance / mouse.radius);
        
        // Repel from mouse
        const force = this.mouseInfluence * 0.21;
        const angle = Math.atan2(dy, dx);
        this.speedX += Math.cos(angle) * force;
        this.speedY += Math.sin(angle) * force;
        
        // Increase activity when mouse is near
        this.activity = Math.min(this.activity + 0.05, 1);
      } else {
        // Gradually reduce mouse influence
        this.mouseInfluence *= 0.95;
        this.activity = Math.max(this.activity - 0.005, 0.3);
      }
      
      // Random direction changes
      this.directionChangeTimer++;
      if (this.directionChangeTimer >= this.directionChangeInterval) {
        // Add small random force to change direction slightly
        this.speedX += (Math.random() - 0.5) * 0.1;
        this.speedY += (Math.random() - 0.5) * 0.1;
        
        // Reset timer and set new interval
        this.directionChangeTimer = 0;
        this.directionChangeInterval = 100 + Math.random() * 200;
      }
      
      // Ensure minimum speed to prevent nodes from stopping
      const currentSpeed = Math.sqrt(this.speedX * this.speedX + this.speedY * this.speedY);
      const minSpeed = 0.15;
      if (currentSpeed < minSpeed) {
        const scale = minSpeed / currentSpeed;
        this.speedX *= scale;
        this.speedY *= scale;
      }
      
      // Apply very light friction to prevent unlimited acceleration
      this.speedX *= 0.995;
      this.speedY *= 0.995;
      
      // Update position
      this.x += this.speedX;
      this.y += this.speedY;
      
      // Boundary checks - wrap around edges
      if (!canvas) return;
      if (this.x < 0) this.x = canvas.width;
      if (this.x > canvas.width) this.x = 0;
      if (this.y < 0) this.y = canvas.height;
      if (this.y > canvas.height) this.y = 0;
      
      // Pulse effect
  if (pulseActive) {
        this.size = Math.min(this.size * 1.03, this.baseSize * 1.8);
      } else {
        this.size = Math.max(this.size * 0.97, this.baseSize);
      }
      
      // Subtle pulsing animation
      this.pulsePhase += 0.015;
    }
    
    draw(ctx, colors) {
      ctx.save();
      ctx.translate(this.x, this.y);
      
      // Debug: log if we're actually drawing nodes
      if (Math.random() < 0.001) {
        console.log('Drawing node at:', this.x, this.y, 'opacity:', this.opacity, 'activity:', this.activity);
      }
      
      // Enhanced glow when mouse is near - increased visibility
      const glowSize = this.size * 4 * (1 + this.mouseInfluence * 0.8);
      const glowOpacity = Math.min(this.opacity * this.activity * (0.9 + this.mouseInfluence * 0.6), 1);
      
      // Node glow - more prominent
      const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, glowSize);
      gradient.addColorStop(0, colors.node + glowOpacity + ')');
      gradient.addColorStop(1, colors.node + '0)');
      
      ctx.beginPath();
      ctx.arc(0, 0, glowSize, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();
      
      // Node core - make it more visible with higher opacity
      const coreSize = this.size * (1 + this.mouseInfluence * 0.5);
      const coreOpacity = Math.min(this.opacity * 1.2, 1); // Increased core opacity
      ctx.beginPath();
      ctx.arc(0, 0, coreSize, 0, Math.PI * 2);
      ctx.fillStyle = colors.node + coreOpacity + ')';
      ctx.fill();
      
      // Inner highlight
      ctx.beginPath();
      ctx.arc(0, 0, coreSize * 0.5, 0, Math.PI * 2);
      ctx.fillStyle = colors.node + (coreOpacity * 0.9) + ')';
      ctx.fill();
      
      ctx.restore();
    }
  }
  
  // Connection class
  class Connection {
    constructor(nodeA, nodeB) {
      this.nodeA = nodeA;
      this.nodeB = nodeB;
      this.strength = Math.random() * 0.4 + 0.3;
      this.pulsePhase = Math.random() * Math.PI * 2;
      this.appearing = true; // Track if connection is appearing
      this.appearProgress = 0; // Progress of appearance animation
    }
    
    update() {
      // Calculate distance
      const dx = this.nodeB.x - this.nodeA.x;
      const dy = this.nodeB.y - this.nodeA.y;
      this.distance = Math.sqrt(dx * dx + dy * dy);
      
      // Update pulse phase
      this.pulsePhase += 0.008;
      
      // Update appearance animation
      if (this.appearing) {
        this.appearProgress += 0.05;
        if (this.appearProgress >= 1) {
          this.appearing = false;
          this.appearProgress = 1;
        }
      }
      
      // Adjust strength based on distance and mouse influence
      const maxDistance = 120;
      if (this.distance < maxDistance) {
        const distanceFactor = 1 - this.distance / maxDistance;
        const mouseFactor = (this.nodeA.mouseInfluence + this.nodeB.mouseInfluence) / 2;
        this.strength = distanceFactor * 0.6 + mouseFactor * 0.2;
      } else {
        this.strength = 0;
      }
    }
    
    draw(ctx, colors) {
      if (this.strength <= 0) return;
      
      ctx.save();
      
      // Enhanced pulse effect for better visibility
      const pulseValue = Math.sin(this.pulsePhase) * 0.3 + 0.7;
  const opacity = Math.min(0.95, this.strength * pulseValue * this.appearProgress * 1.0);
      
      // Debug: log if we're actually drawing
      if (Math.random() < 0.001) {
        console.log('Drawing edge with opacity:', opacity, 'strength:', this.strength);
      }
      
      // Draw connection line with better visibility
      ctx.beginPath();
      ctx.moveTo(this.nodeA.x, this.nodeA.y);
      ctx.lineTo(this.nodeB.x, this.nodeB.y);
      
      // Enhanced line width based on strength
  ctx.lineWidth = Math.max(2.0, this.strength * 4.5);
      ctx.strokeStyle = colors.edge + opacity + ')';
      ctx.stroke();
      
      ctx.restore();
    }
  }

  // Initialize neural network
  const initNeuralNetwork = () => {
    const canvas = canvasRef.current;
    if (!canvas) {
      console.log('Cannot initialize neural network: canvas is null');
      return;
    }
    
    console.log('Initializing neural network with canvas size:', canvas.width, 'x', canvas.height);
    
    const newNodes = [];
    const newConnections = [];
    
    // Create nodes - increased count with forced visibility
    const nodeCount = 50; // Reduced for easier debugging
    for (let i = 0; i < nodeCount; i++) {
      const node = new Node(
        Math.random() * canvas.width,
        Math.random() * canvas.height
      );
      // Force high visibility for testing
      node.opacity = 1.0;
      node.activity = 1.0;
      node.size = 5; // Larger for visibility
      newNodes.push(node);
    }
    
    console.log('Created', newNodes.length, 'nodes');
    
    // Create connections between nearby nodes
    for (let i = 0; i < newNodes.length; i++) {
      for (let j = i + 1; j < newNodes.length; j++) {
        const dx = newNodes[i].x - newNodes[j].x;
        const dy = newNodes[i].y - newNodes[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 200) { // Increased connection distance
          const connection = new Connection(newNodes[i], newNodes[j]);
          connection.strength = 0.8; // Force high strength
          connection.appearProgress = 1.0; // Fully appeared
          newConnections.push(connection);
        }
      }
    }
    
  console.log('Created', newConnections.length, 'connections');

  // Update refs first (used by RAF loop)
  nodesRef.current = newNodes;
  connectionsRef.current = newConnections;
    
  // Optionally update state (for dev tools / future UI hooks)
  setNodes(newNodes);
  setConnections(newConnections);
  };

  // Draw background
  const drawBackground = (ctx) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const gradient = ctx.createRadialGradient(
      canvas.width / 2, canvas.height / 2, 0,
      canvas.width / 2, canvas.height / 2, 
      Math.max(canvas.width, canvas.height)
    );
    gradient.addColorStop(0, currentColors.background.start);
    gradient.addColorStop(1, currentColors.background.end);
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  };

  // Draw grid overlay
  const drawGrid = (ctx) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    ctx.strokeStyle = currentColors.grid;
    ctx.lineWidth = 1;
    
    const gridSize = 50;
    
    // Vertical lines
    for (let x = 0; x < canvas.width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }
    
    // Horizontal lines
    for (let y = 0; y < canvas.height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }
  };

  // Draw mouse influence area
  const drawMouseInfluence = (ctx) => {
    const { x, y, radius } = mouseRef.current;
    if (x < 0 || y < 0) return;
    
    ctx.save();
    
    // Mouse influence circle
    const gradient = ctx.createRadialGradient(
      x, y, 0,
      x, y, radius
    );
    gradient.addColorStop(0, currentColors.mouseInfluence.start);
    gradient.addColorStop(1, currentColors.mouseInfluence.end);
    
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = gradient;
    ctx.fill();
    
    // Mouse connections to nearby nodes
    let connectionCount = 0;
    const maxConnections = 15;
    
  // Use ref to ensure latest nodes list
  nodesRef.current.forEach(node => {
      if (connectionCount >= maxConnections) return;
      
      const dx = node.x - x;
      const dy = node.y - y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < radius) {
        const strength = 1 - (distance / radius);
        
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(node.x, node.y);
        
        const gradient = ctx.createLinearGradient(
          x, y,
          node.x, node.y
        );
        
        gradient.addColorStop(0, currentColors.mouseConnection.start + (strength * 0.25) + ')');
        gradient.addColorStop(1, currentColors.mouseConnection.end + (strength * 0.08) + ')');
        
        ctx.strokeStyle = gradient;
        ctx.lineWidth = strength * 1.2;
        ctx.stroke();
        
        connectionCount++;
      }
    });
    
    ctx.restore();
  };

  // Animation loop
  const animate = () => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    
    if (!ctx || !canvas) {
      animationRef.current = requestAnimationFrame(animate);
      return;
    }
    
  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Background gradient
  drawBackground(ctx);
    
  drawMouseInfluence(ctx);
    
    // Update and draw connections
    let visibleConnections = 0;
  connectionsRef.current.forEach(connection => {
      connection.update();
      if (connection.strength > 0) {
        connection.draw(ctx, currentColors);
        visibleConnections++;
      }
    });
    
    // Update and draw nodes
    let visibleNodes = 0;
  nodesRef.current.forEach(node => {
      node.update(mouseRef.current, canvas);
      node.draw(ctx, currentColors);
      visibleNodes++;
    });
    
  // Optional: lightweight sampling log (disabled)
  // if (Math.random() < 0.005) console.log('RAF', { nodes: visibleNodes, connections: visibleConnections });
    
    drawGrid(ctx);
    
    animationRef.current = requestAnimationFrame(animate);
  };

  // Global mouse move (use ref to avoid stale state in RAF loop)
  const handleGlobalMouseMove = useCallback((e) => {
    mouseRef.current.x = e.clientX;
    mouseRef.current.y = e.clientY;
  }, []);

  // Handle touch move for mobile devices
  const handleTouchMove = (e) => {
    const touch = e.touches[0];
    if (touch) {
      mouseRef.current.x = touch.clientX;
      mouseRef.current.y = touch.clientY;
    }
  };

  // Handle global touch move
  const handleGlobalTouchMove = useCallback((e) => {
    const touch = e.touches[0];
    if (touch) {
      mouseRef.current.x = touch.clientX;
      mouseRef.current.y = touch.clientY;
    }
  }, []);

  // Handle mouse leave
  const handleMouseLeave = useCallback(() => {
    mouseRef.current.x = -1000;
    mouseRef.current.y = -1000;
  }, []);

  // Handle window resize
  const handleResize = () => {
    const canvas = canvasRef.current;
    if (canvas) {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
  initNeuralNetwork();
  // Ensure refs are in sync after resize
  nodesRef.current = nodesRef.current;
  connectionsRef.current = connectionsRef.current;
    }
  };

  // Initialize on mount
  useEffect(() => {
    // Small delay to ensure DOM is ready
    const initTimeout = setTimeout(() => {
      const canvas = canvasRef.current;
      console.log('Background3D useEffect triggered, canvas:', canvas);
      
      if (canvas) {
        // Set canvas dimensions
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        console.log('Canvas dimensions set to:', canvas.width, 'x', canvas.height);
        
        // Test basic canvas functionality
        const ctx = canvas.getContext('2d');
        if (ctx) {
          console.log('Canvas context obtained successfully');
          // Draw immediate test
          ctx.fillStyle = 'red';
          ctx.fillRect(50, 50, 100, 100);
          console.log('Test rectangle drawn');
        } else {
          console.error('Failed to get canvas context');
        }
        
        initNeuralNetwork();
        animate();
      } else {
        console.error('Canvas ref is null in useEffect');
      }
    }, 100);

    // Global listeners so canvas senses pointer across page
    window.addEventListener('mousemove', handleGlobalMouseMove);
    window.addEventListener('mouseleave', handleMouseLeave);
    window.addEventListener('touchmove', handleGlobalTouchMove, { passive: true });
    window.addEventListener('touchend', handleMouseLeave);
    window.addEventListener('resize', handleResize);
    
    // Auto pulse simulation
    const pulseInterval = setInterval(() => {
      setPulseActive(true);
      setTimeout(() => {
        setPulseActive(false);
      }, 1000);
    }, 5000 + Math.random() * 3000);
    
    // Clean up
    return () => {
      clearTimeout(initTimeout);
      window.removeEventListener('mousemove', handleGlobalMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
      window.removeEventListener('touchmove', handleGlobalTouchMove);
      window.removeEventListener('touchend', handleMouseLeave);
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationRef.current);
      clearInterval(pulseInterval);
    };
  }, [currentTheme]); // Re-run when theme changes

  return (
    <div style={{ 
      position: 'fixed', 
      top: 0,
      left: 0,
      width: '100vw', 
      height: '100vh', 
      overflow: 'hidden',
      zIndex: 0,
      pointerEvents: 'none',
      background: currentTheme === 'dark' ? '#000' : '#fff'
    }}>
      <canvas
        ref={canvasRef}
        style={{ 
          position: 'absolute', 
          top: 0, 
          left: 0, 
          width: '100%', 
          height: '100%',
          display: 'block',
          pointerEvents: 'none'
        }}
      />
    </div>
  );
};

export default Background3D;