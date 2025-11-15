const isVercel = !!process.env.VERCEL;
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['@sparticuz/chromium', 'puppeteer-core'],
  },
  reactStrictMode: false,
  ...(isVercel ? {} : { distDir: ".next-build" }),
  

  async rewrites() {
    const rewrites = [];
    const defaultApiBase = 'https://presenton-1.onrender.com';
    const apiBase = process.env.FASTAPI_BASE_URL || process.env.NEXT_PUBLIC_FASTAPI_URL || defaultApiBase;

    if (apiBase) {
      rewrites.push(
        {
          source: '/api/v1/:path*',
          destination: `${apiBase}/api/v1/:path*`,
        },
        {
          source: '/app_data/:path*',
          destination: `${apiBase}/app_data/:path*`,
        },
      );
    }

    if (process.env.NODE_ENV === 'development') {
      rewrites.push({
        source: '/app_data/fonts/:path*',
        destination: 'http://localhost:8000/app_data/fonts/:path*',
      });
    }

    return rewrites;
  },

  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: "https",
        hostname: "pub-7c765f3726084c52bcd5d180d51f1255.r2.dev",
      },
      {
        protocol: "https",
        hostname: "pptgen-public.ap-south-1.amazonaws.com",
      },
      {
        protocol: "https",
        hostname: "pptgen-public.s3.ap-south-1.amazonaws.com",
      },
      {
        protocol: "https",
        hostname: "img.icons8.com",
      },
      {
        protocol: "https",
        hostname: "present-for-me.s3.amazonaws.com",
      },
      {
        protocol: "https",
        hostname: "yefhrkuqbjcblofdcpnr.supabase.co",
      },
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
      {
        protocol: "https",
        hostname: "picsum.photos",
      },
      {
        protocol: "https",
        hostname: "unsplash.com",
      },
    ],
  },
  
};

export default nextConfig;
