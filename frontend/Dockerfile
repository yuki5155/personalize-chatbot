# Use Node.js LTS (v22.15.0) full image for development
FROM node:22.15.0

# Create app directory
WORKDIR /usr/src/app

# Check if package.json exists, if not create a basic one
COPY package*.json ./
RUN if [ ! -f package.json ]; then \
      echo '{"name":"vue-app","version":"1.0.0","private":true,"scripts":{"dev":"vue-cli-service serve","build":"vue-cli-service build"},"dependencies":{"vue":"^3.3.4"},"devDependencies":{"@vue/cli-service":"^5.0.8"}}' > package.json; \
    fi

# Install dependencies including development dependencies
RUN npm install

# Bundle app source
COPY . .

# Create a non-root user with limited permissions
RUN groupadd -g 1001 nodejs && \
    useradd -u 1001 -g nodejs -s /bin/bash -m nodejs

# Change ownership to the non-root user
RUN chown -R nodejs:nodejs /usr/src/app

# Switch to non-root user
USER nodejs



# Command for development
CMD [ "npm", "run", "dev" ] 