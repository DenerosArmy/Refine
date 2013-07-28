package com.example.refine;

import com.example.refine.util.SystemUiHider;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.app.*;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.*;
import android.graphics.*;
import android.graphics.drawable.*;
import android.net.http.AndroidHttpClient;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.net.Uri;
import android.os.*;
import android.provider.Settings.Secure;
import android.util.Log;
import android.view.*;
import android.view.MenuItem.OnActionExpandListener;
import android.view.View.OnClickListener;
import android.view.inputmethod.EditorInfo;
import android.widget.*;
import android.widget.SearchView.OnQueryTextListener;
import java.io.*;
import java.util.List;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Hashtable;
import org.apache.http.*;
import org.apache.http.client.*;
import org.apache.http.impl.client.DefaultHttpClient;
import android.annotation.TargetApi;
import android.os.Build;
import android.os.Handler;
import android.view.MotionEvent;
import android.view.View;
import java.net.URI;
import org.apache.http.message.BasicNameValuePair;
import java.util.Arrays;
import android.provider.Settings.Secure;

import com.codebutler.android_websockets.*;


/**
 * An example full-screen activity that shows and hides the system UI (i.e.
 * status bar and navigation/system bar) with user interaction.
 *
 * @see SystemUiHider
 */
public class Refine extends Activity {
    /**
     * Whether or not the system UI should be auto-hidden after
     * {@link #AUTO_HIDE_DELAY_MILLIS} milliseconds.
     */
    private static final boolean AUTO_HIDE = true;
    private static Context context;
    private WifiManager wifiManager;
    private boolean connected;
    private long lastTime;
    /**
     * If {@link #AUTO_HIDE} is set, the number of milliseconds to wait after
     * user interaction before hiding the system UI.
     */
    private static final int AUTO_HIDE_DELAY_MILLIS = 3000;

    /**
     * If set, will toggle the system UI visibility upon interaction. Otherwise,
     * will show the system UI visibility upon interaction.
     */
    private static final boolean TOGGLE_ON_CLICK = true;

    /**
     * The flags to pass to {@link SystemUiHider#getInstance}.
     */
    private static final int HIDER_FLAGS = SystemUiHider.FLAG_HIDE_NAVIGATION;

    /**
     * The instance of the {@link SystemUiHider} for this activity.
     */
    private SystemUiHider mSystemUiHider;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
 
        wifiManager = (WifiManager) getSystemService(Context.WIFI_SERVICE);
        final String TAG = "MonkeyPenis";
        List<BasicNameValuePair> extraHeaders = Arrays.asList(
        	    new BasicNameValuePair("Cookie", "session=abcd")
        	);
        final WebSocketClient client = new WebSocketClient(URI.create("ws://198.61.194.98:9000/push_updates"), new WebSocketClient.Listener() {
        	
            @Override
          
            public void onConnect() {
                Log.d(TAG, "Connected!");
                connected = true;
            }

            @Override
            public void onMessage(String message) {
                Log.d(TAG, String.format("Got string message! %s", message));
            }

            @Override 
            public void onMessage(byte[] message){
            	
            }

            @Override
            public void onDisconnect(int code, String reason) {
                Log.d(TAG, String.format("Disconnected! Code: %d Reason: %s", code, reason));
                connected = false;
            }

            @Override
            public void onError(Exception error) {
                Log.e(TAG, "Error!", error);
            }

        }, extraHeaders);

        Thread t = new Thread(new Runnable() 
        { 
        	@Override 
        		public void run() {
        		
        		while (true) {
        			wifiManager.startScan();
        			try {
        				Thread.sleep(2);
					} catch(InterruptedException e){
					
						
					}
        			
        			List<ScanResult> scanResults = wifiManager.getScanResults();
        			for (ScanResult result: scanResults) {
        			
        					if (result.SSID.equals("Jifi") && !connected) { 
        						Log.i("MonkeyPenis", "TRYING TO CONNECT");
        						client.connect();
        						
        						
        					}
        					
        					if (connected && result.SSID.equals("Jifi")) {
        						if (result.timestamp != lastTime) { 
        						
        						
        						if (result.level > -50) { 
        							client.send("kevid" + "|" + result.SSID);
        						} else { 
        							client.send("kevid" + "|" + "");
        						}
        						}
        					}
        					
        			}
        		}
        	}
        });
        					
        					
      
        
        t.start();
        setContentView(R.layout.activity_refine);

        final View controlsView = findViewById(R.id.fullscreen_content_controls);
        final View contentView = findViewById(R.id.fullscreen_content);

        // Set up an instance of SystemUiHider to control the system UI for
        // this activity.
        mSystemUiHider = SystemUiHider.getInstance(this, contentView, HIDER_FLAGS);
        mSystemUiHider.setup();
        mSystemUiHider
                .setOnVisibilityChangeListener(new SystemUiHider.OnVisibilityChangeListener() {
                    // Cached values.
                    int mControlsHeight;
                    int mShortAnimTime;

                    @Override
                    @TargetApi(Build.VERSION_CODES.HONEYCOMB_MR2)
                    public void onVisibilityChange(boolean visible) {
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.HONEYCOMB_MR2) {
                            // If the ViewPropertyAnimator API is available
                            // (Honeycomb MR2 and later), use it to animate the
                            // in-layout UI controls at the bottom of the
                            // screen.
                            if (mControlsHeight == 0) {
                                mControlsHeight = controlsView.getHeight();
                            }
                            if (mShortAnimTime == 0) {
                                mShortAnimTime = getResources().getInteger(
                                        android.R.integer.config_shortAnimTime);
                            }
                            controlsView.animate()
                                    .translationY(visible ? 0 : mControlsHeight)
                                    .setDuration(mShortAnimTime);
                        } else {
                            // If the ViewPropertyAnimator APIs aren't
                            // available, simply show or hide the in-layout UI
                            // controls.
                            controlsView.setVisibility(visible ? View.VISIBLE : View.GONE);
                        }

                        if (visible && AUTO_HIDE) {
                            // Schedule a hide().
                            delayedHide(AUTO_HIDE_DELAY_MILLIS);
                        }
                    }
                });

        // Set up the user interaction to manually show or hide the system UI.
        contentView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (TOGGLE_ON_CLICK) {
                    mSystemUiHider.toggle();
                } else {
                    mSystemUiHider.show();
                }
            }
        });

        // Upon interacting with UI controls, delay any scheduled hide()
        // operations to prevent the jarring behavior of controls going away
        // while interacting with the UI.
        findViewById(R.id.dummy_button).setOnTouchListener(mDelayHideTouchListener);
    }

    @Override
    protected void onPostCreate(Bundle savedInstanceState) {
        super.onPostCreate(savedInstanceState);

        // Trigger the initial hide() shortly after the activity has been
        // created, to briefly hint to the user that UI controls
        // are available.
        delayedHide(100);
    }


    /**
     * Touch listener to use for in-layout UI controls to delay hiding the
     * system UI. This is to prevent the jarring behavior of controls going away
     * while interacting with activity UI.
     */
    View.OnTouchListener mDelayHideTouchListener = new View.OnTouchListener() {
        @Override
        public boolean onTouch(View view, MotionEvent motionEvent) {
            if (AUTO_HIDE) {
                delayedHide(AUTO_HIDE_DELAY_MILLIS);
            }
            return false;
        }
    };

    Handler mHideHandler = new Handler();
    Runnable mHideRunnable = new Runnable() {
        @Override
        public void run() {
            mSystemUiHider.hide();
        }
    };

    /**
     * Schedules a call to hide() in [delay] milliseconds, canceling any
     * previously scheduled calls.
     */
    private void delayedHide(int delayMillis) {
        mHideHandler.removeCallbacks(mHideRunnable);
        mHideHandler.postDelayed(mHideRunnable, delayMillis);
    }
}