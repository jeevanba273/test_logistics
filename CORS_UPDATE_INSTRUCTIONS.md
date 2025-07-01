# CORS Configuration Update Required

Your LogiTrack application is now deployed, but you need to update the CORS settings to allow your frontend to communicate with the backend.

## Required Action:

### Update Railway Environment Variables

1. **Go to your Railway dashboard**: https://railway.app/dashboard
2. **Select your LogiTrack project**
3. **Navigate to the Variables tab**
4. **Add or update the following environment variable**:

```
CORS_ORIGINS=https://mad-logistics.netlify.app
```

### Steps:
1. Click "New Variable" or edit existing `CORS_ORIGINS`
2. Set the value to: `https://mad-logistics.netlify.app`
3. Click "Add" or "Save"
4. Railway will automatically redeploy your backend

### Verification:
After the redeployment (usually takes 1-2 minutes):
1. Visit: https://mad-logistics.netlify.app/
2. Try logging in with demo credentials:
   - **Admin**: `admin01` / `1234`
   - **User**: `user01` / `1234`

## Current Status:
✅ **Frontend**: Deployed on Netlify  
✅ **Backend**: Deployed on Railway  
⏳ **CORS**: Needs to be updated (this step)  

## Demo Credentials:
- **Admin User**: username: `admin01`, password: `1234`
- **Regular User**: username: `user01`, password: `1234`

Once you've updated the CORS settings, your full-stack LogiTrack application will be fully functional!