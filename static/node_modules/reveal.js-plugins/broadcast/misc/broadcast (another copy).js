/*****************************************************************
** Author: Asvin Goel, goel@telematique.eu
**
** A plugin for broadcasting reveal.js presentations
**
** Version: 0.1
** 
** License: MIT license (see LICENSE.md)
**
** Credits: 
** RTCMultiConnect effect by Muaz Khan
******************************************************************/

var RevealBroadcast = window.RevealBroadcast || (function(){
	var path = scriptPath();
	function scriptPath() {
		// obtain plugin path from the script element
		var src;
		if (document.currentScript) {
			src = document.currentScript.src;
		} else {
			var sel = document.querySelector('script[src$="/broadcast.js"]')
			if (sel) {
				src = sel.src;
			}
		}

		var path = typeof src === undefined ? src
			: src.slice(0, src.lastIndexOf("/") + 1);
//console.log("Path: " + path);
		return path;
	}

/*****************************************************************
** Initialisation
******************************************************************/
	var config = Reveal.getConfig().broadcast || {};

	var master = false;
	var broadcastId;
	if ( config.broadcastId ) broadcastId = config.broadcastId;

	if ( config.master ) master = config.master;

	var connection = new RTCMultiConnection(null, {
		useDefaultDevices: true // if we don't need to force selection of specific devices
	});
//	connection.enableLogs = true;

	// its mandatory in v3
	connection.enableScalableBroadcast = true;

	// each relaying-user should serve only 1 users
	connection.maxRelayLimitPerUser = 1;

	// we don't need to keep room-opened
	// scalable-broadcast.js will handle stuff itself.
	connection.autoCloseEntireSession = true;

	// by default, socket.io server is assumed to be deployed on your own URL
	connection.socketURL = '/';
	// comment-out below line if you do not have your own socket.io server
//	connection.socketURL = 'https://rtcmulticonnection.herokuapp.com:443/';
	if ( config.socketURL ) connection.socketURL = config.socketURL;

	connection.session = {
        	audio: true,
        	video: true,
        	oneway: true
        };
	if ( config.audio ) connection.session.audio = config.audio;
	if ( config.audio ) connection.session.audio = config.audio;


	connection.socketMessageEvent = 'scalable-media-broadcast-demo';
	connection.socketCustomEvent = connection.channel;
//            connection.connectSocket(function(socket) { /* ... */ };
/// Begin connect
	    // Socket connection is now opened
//console.log( "Socket: " + connection.getSocket() );

function connect( master ) {
	    if ( master ) {
		this.master = master; // TODO: Do not allow master to be set.
	    }
            // user need to connect server, so that others can reach him.
            connection.connectSocket(function(socket) {
		// Receive custom event
                socket.on(connection.socketCustomEvent, function(message) {
			console.log("Received: " + JSON.stringify( message ) );
			if ( !master && message.type == "reveal-state-changed" ) {
				Reveal.setState(message.state);
			}
                });

                socket.on('logs', function(log) {
                    document.getElementById('broadcast-info').innerHTML = log.replace(/</g, '----').replace(/>/g, '___').replace(/----/g, '<span style="color:red;">').replace(/___/g, '</span>');
                });

                // this event is emitted when a broadcast is absent.
                socket.on('start-broadcasting', function(typeOfStreams) {
                    console.log('start-broadcasting', typeOfStreams);

                    // host i.e. sender should always use this!
                    connection.sdpConstraints.mandatory = {
                        OfferToReceiveVideo: false,
                        OfferToReceiveAudio: false
                    };
                    connection.session = typeOfStreams;

                    // "open" method here will capture media-stream
                    // we can skip this function always; it is totally optional here.
                    // we can use "connection.getUserMediaHandler" instead
                    connection.open(connection.userid, function() {
console.log("Connection opened: " + connection.sessionid);
                    });
                });

                // this event is emitted when a broadcast is already created.
                socket.on('join-broadcaster', function(hintsToJoinBroadcast) {
                    console.log('join-broadcaster', hintsToJoinBroadcast);

                    connection.session = hintsToJoinBroadcast.typeOfStreams;
                    connection.sdpConstraints.mandatory = {
                        OfferToReceiveVideo: !!connection.session.video,
                        OfferToReceiveAudio: !!connection.session.audio
                    };
                    connection.broadcastId = hintsToJoinBroadcast.broadcastId;
                    connection.join(hintsToJoinBroadcast.userid);
                });

                socket.on('rejoin-broadcast', function(broadcastId) {
                    console.log('rejoin-broadcast', broadcastId);

                    connection.attachStreams = [];
                    socket.emit('check-broadcast-presence', broadcastId, function(isBroadcastExists) {
                        if(!isBroadcastExists) {
                            // the first person (i.e. real-broadcaster) MUST set his user-id
                            connection.userid = broadcastId;
                        }

                        socket.emit('join-broadcast', {
                            broadcastId: broadcastId,
                            userid: connection.userid,
                            typeOfStreams: connection.session
                        });
                    });
                });

                socket.on('broadcast-stopped', function(broadcastId) {
                    // alert('Broadcast has been stopped.');
                    // location.reload();
                    console.error('broadcast-stopped', broadcastId);
                    alert('This broadcast has been stopped.');
                });

		// establish connection 
                socket.emit('check-broadcast-presence', broadcastId, function(isBroadcastExists) {
		if ( master ) {
                    if(!isBroadcastExists) {
                        // the first person (i.e. real-broadcaster) MUST set his user-id
	                console.log('Start broadcast', broadcastId, isBroadcastExists);
                        connection.userid = broadcastId;
                	socket.emit('join-broadcast', {
                        	broadcastId: broadcastId,
                        	userid: connection.userid,
                        	typeOfStreams: connection.session
                    	});
                    }
		    else {
                    	alert('Broadcast already exists!');
		    }

		function post() {
	                socket.emit(connection.socketCustomEvent, {
	                        sender: connection.userid,
	                        type: "reveal-state-changed",
	                        state: Reveal.getState()
	                });

	
		};
		
		// Monitor events that trigger a change in state
		Reveal.addEventListener( 'slidechanged', post );
		Reveal.addEventListener( 'fragmentshown', post );
		Reveal.addEventListener( 'fragmenthidden', post );
		Reveal.addEventListener( 'overviewhidden', post );
		Reveal.addEventListener( 'overviewshown', post );
		Reveal.addEventListener( 'paused', post );
		Reveal.addEventListener( 'resumed', post );

		}
		else {
		    if (isBroadcastExists) {
	            	console.log('Join broadcast', broadcastId, isBroadcastExists);


                    	socket.emit('join-broadcast', {
                        	broadcastId: broadcastId,
                        	userid: connection.userid,
                        	typeOfStreams: connection.session
                    	});
		    }
		    else {
                    	alert('Broadcast does not yet exist!');
		    }
		}
                });

            });
}
/// End connect

	var videoPreview = document.getElementById('broadcast-video');

	connection.onstream = function(event) {
		if(connection.isInitiator && event.type !== 'local') {
			return;
		}

		if(event.mediaElement) {
			event.mediaElement.pause();
			delete event.mediaElement;
		}

		connection.isUpperUserLeft = false;
		videoPreview.src = URL.createObjectURL(event.stream);
		videoPreview.play();

		videoPreview.userid = event.userid;

		if(event.type === 'local') {
			videoPreview.muted = true;
		}

		if (connection.isInitiator == false && event.type === 'remote') {
			// he is merely relaying the media
			connection.dontCaptureUserMedia = true;
			connection.attachStreams = [event.stream];
			connection.sdpConstraints.mandatory = {
				OfferToReceiveAudio: false,
				OfferToReceiveVideo: false
			};

			var socket = connection.getSocket();
			socket.emit('can-relay-broadcast');

			if(connection.DetectRTC.browser.name === 'Chrome') {
				connection.getAllParticipants().forEach(function(p) {
					if(p + '' != event.userid + '') {
						var peer = connection.peers[p].peer;
						peer.getLocalStreams().forEach(function(localStream) {
							peer.removeStream(localStream);
						});
						peer.addStream(event.stream);
						connection.dontAttachStream = true;
						connection.renegotiate(p);
						connection.dontAttachStream = false;
					}
				});
			}

			if(connection.DetectRTC.browser.name === 'Firefox') {
				// Firefox is NOT supporting removeStream method
				// that's why using alternative hack.
				// NOTE: Firefox seems unable to replace-tracks of the remote-media-stream
				// need to ask all deeper nodes to rejoin
				connection.getAllParticipants().forEach(function(p) {
					if(p + '' != event.userid + '') {
						connection.replaceTrack(event.stream, p);
					}
				});
			}

			// Firefox seems UN_ABLE to record remote MediaStream
			// WebAudio solution merely records audio
			// so recording is skipped for Firefox.
			if(connection.DetectRTC.browser.name === 'Chrome') {
				repeatedlyRecordStream(event.stream);
			}
		}
	};

	connection.onstreamended = function() {};

	connection.onleave = function(event) {
		if(event.userid !== videoPreview.userid) return;

		var socket = connection.getSocket();
                socket.emit('can-not-relay-broadcast');

		connection.isUpperUserLeft = true;
	};

/*****************************************************************
** Master
******************************************************************/
	var numberOfViewers = 0;
	connection.onNumberOfBroadcastViewersUpdated = function(event) {
                if (!connection.isInitiator) return;
		numberOfViewers = event.numberOfBroadcastViewers;
console.log("Numberof viewers: " + numberOfViewers);
	};

	this.connect = connect;
	return this;
})();

