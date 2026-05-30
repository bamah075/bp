FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package.json
COPY client/package.json client/package.json

# Install dependencies
RUN npm install
RUN cd client && npm install && cd ..

# Copy source code
COPY . .

# Build client
RUN cd client && npm run build && cd ..

# Expose port
EXPOSE 3001

# Start server
CMD ["npm", "start"]
