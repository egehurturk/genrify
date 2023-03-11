import { useEffect, useState } from 'react'
import Modal from 'react-modal'

Modal.setAppElement("#root")

const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
    border: '0px solid #ccc',
    backgroundColor: 'rgba(100, 100, 100, 0)'
  },
  overlay: {
    backgroundColor: 'rgba(150, 150, 150, 0.55)'
  }
};

function isJsonString(str) {
  try {
      JSON.parse(str);
  } catch (e) {
      return false;
  }
  return true;
}

function getExtension(filename) {
  return filename.split('.').pop()
}

function properName(filename) {
  if (filename.length <= 15) {
    return filename
  }
  return filename.substring(0, 15) + "... .mp3";
}

function checkFile(file) {
  let msg = "";
  if (getExtension(file.name).toLowerCase() !== "mp3") {
    msg = `${file.name} is not a mp3 file. Only mp3 files are accepted for upload`;
    return [false, msg];
  } else if (file.size >= 10000000) {
    msg = `${file.name} exceeds the 10MB file size limit`;
    return [false, msg];
  } else {
    return [true, msg];
  }
}


export default function Example() {

  const [youtubeLink, setYoutubeLink]   = useState("")
  const [youtubeLinkUploaded, setYoutubeLinkUploaded] =  useState(false)
  const [fileUploaded, setFileUploaded] =  useState(false)
  const [file, setFile] = useState();
  const [spinner, setSpinner] = useState(false);
  const [modalShow, setModelShow] = useState(false);
  const [modalData, setModelData] = useState("");

  useEffect(() => {
    // console.log(modalData)
    // console.log(toType(modalData))
  }, [modalData])

  const handleSubmit = (event) => {
    event.preventDefault();
    setSpinner(true);

    const data = new FormData(event.target);
    fetch('http://127.0.0.1:8000/api/classify', {
      method: 'POST',
      body: data,
    })
    .then( res => res.json())
    .then( data => {
      setSpinner(false); 
      setModelData(data);
      setModelShow(true);
      setYoutubeLinkUploaded(false);
      setFileUploaded(false);
      setFile();
      setYoutubeLink("")
    } )
    .catch(error => {
      setModelData(error);
      setModelShow(true);
      setSpinner(false); 
      setYoutubeLinkUploaded(false);
      setFileUploaded(false);
      setFile();
      setYoutubeLink("");
    })
  }

  const handleFileUpload = (event) => {
    if (event.target.files) {
      const [check, msg] = checkFile(event.target.files[0]);

      if (check) {
          setFile(event.target.files[0]);
          setFileUploaded(true);
      }
      else {
        setModelData(msg);
        setModelShow(true);
      }
    } 
    else {
      alert("No files are uploaded")
    }
  }

  const handleRemoveFileUpload = (event) => {
    event.preventDefault();
    setFile(null);
    setFileUploaded(false); 
  }

  const handleInputChange = (event) => {
    if (event.target.value !== "") {
      setYoutubeLink(event.target.value);
      setYoutubeLinkUploaded(true);
    } else {
      setYoutubeLinkUploaded(false);
      setYoutubeLink("");
    }
  }


  let klass_div = "mt-2 flex justify-center rounded-md border-2 border-dashed border-gray-300 px-6 pt-5 pb-6";
  if (youtubeLinkUploaded) {
    klass_div += " cursor-not-allowed bg-gray-700 ring-gray-200 pb-6";
  }

  let klass_upload = "relative rounded-md font-medium text-indigo-400 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2"
  if (youtubeLinkUploaded) {
    klass_upload += " cursor-not-allowed ";
  } else {
    klass_upload += " cursor-pointer hover:text-indigo-500";
  }

  let klass_svg = "w-5 cursor-pointer hover:text-gray-300 h-5 text-white";
  if (fileUploaded) {
  } else {
    klass_svg += " hidden"
  }


  let klass_svg_loader = "text-xs w-5 h-5 mr-2 text-white animate-spin dark:text-gray-400 fill-blue-500"
  if (!spinner) {
    klass_svg_loader += " hidden"
  }

  return (
    <>
      <div className="min-h-full">

        <div className="bg-gray-800 pb-32">
          <header className="py-10">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              <h1 className="text-6xl text-center font-bold tracking-tight text-white">Genrify</h1>
            </div>
          </header>
        </div>

        {/* MAIN CONTENT */}
        <main className="-mt-32">
          <div className="mx-auto max-w-5xl px-4 pb-12 sm:px-6 lg:px-8">
            <form onSubmit={handleSubmit} method="post" className="space-y-8" encType='multipart/form-data'>
              <div className="space-y-8">

                {/* FORM BLOCK */}
                <div className="pt-8">
                  <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                    <div className="sm:col-span-6 flex rounded-md shadow-sm">
                      <div className="mt-4 relative flex flex-grow items-stretch focus-within:z-10">
                        <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-5">
                          <span className="text-gray-500 sm:text-sm">youtube-url: </span>
                        </div>
                        <input
                          type="text"
                          name="song-link-text"
                          id="song-link-text"
                          disabled={fileUploaded}
                          autoComplete="text"
                          value={youtubeLink}
                          onChange={handleInputChange}
                          placeholder='Enter YouTube link'
                          className="block w-full bg-gray-700 rounded-lg pl-28 text-gray-300 shadow-sm placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-300 sm:text-sm sm:leading-6 disabled:bg-gray-600 disabled:cursor-not-allowed disabled:text-white disabled:border-dashed disabled:border-2 disabled:ring-gray-200"
                        />
                      </div>
                     
                    </div>
                  </div>
                </div>

                {/* OR  */}
                <div className='flex items-center justify-center'>
                    <div className="mt-4 mb-2 w-1/12 bg-gray-500 rounded-xl">
                      <h3 className='text-center text-white'>OR</h3>
                    </div>
                </div>

                {/* UPLOAD BLOCK */}
                <div className="mt-6 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                  <div className="sm:col-span-6">
                    <div className={klass_div}>
                      <div className="space-y-1 text-center">
                        <svg
                          className="mx-auto h-12 w-12 text-gray-400"
                          stroke="currentColor"
                          fill="none"
                          viewBox="0 0 48 48"
                          aria-hidden="true"
                        >
                          <path
                            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                            strokeWidth={2}
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          />
                        </svg>
                        <div className="flex text-sm text-gray-600">
                          <label
                            htmlFor="file-upload"
                            className={klass_upload}
                          >
                            <span>Upload a file</span>
                            <input
                              id="file-upload"
                              name="file-upload"
                              onChange={handleFileUpload}
                              disabled={youtubeLinkUploaded}
                              type="file" 
                              // TODO: CHANGE HERE
                              className="sr-only" />
                          </label>
                          <p className="pl-1">or drag and drop</p>
                          {/* <p className="text-gray-200 pl-1">{file && `${file.name} - ${file.type} - ${file.size}`}</p> */}
                        </div>
                        <div className='flex justify-center justify-content'>
                            <svg onClick={handleRemoveFileUpload} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className={klass_svg}>
                              <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                            </svg>
                            <p className="text-gray-200 text-sm">
                              {file && `${properName(file.name)}`}
                            </p> 
                        </div>
                          <p className="text-xs text-gray-500">MP3 up to 10MB</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* <Modal title="There were 2 errors with your submission" onClose={() => setModelShow(false)} show={modalShow}>
                    {modalData}
                </Modal> */}

                {/* SUBMIT button */}
                <div>
                  <div className='flex justify-center justify-content'>
                        <button
                          type="submit"
                          className="flex w-full justify-center rounded-md bg-indigo-600 py-2 px-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                        >
                           <svg aria-hidden="true" className={klass_svg_loader} viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                          </svg>
                          Search
                        </button>
                  </div>
                </div>

                <Modal closeTimeoutMS={300} isOpen={modalShow} style={customStyles} onRequestClose={() => setModelShow(false)} shouldCloseOnOverlayClick={true}>
                  <div className="pt-8 pb-10 pr-10 pl-10 rounded-md bg-green-200 p-4">
                      <div className="flex justify-between">
                    
                      <div className="ml-3">
                          <div className="mt-2 text-sm text-gray-700">
                          <ul role="list" className="list-disc space-y-1 pl-5">
                              {
                                isJsonString(modalData)
                                      ? (<li>{`${JSON.parse(modalData).detail}`}</li>)
                                      : (<li>{`${modalData}`}</li>)
                              } 
                          </ul>
                          </div>
                      </div>
                      </div>
                  </div>
                </Modal>  
              </div>
            </form>
          </div>
        </main>
      </div>
    </>
  )
}


// FIXME: when cross is selected while removing uploaded file, it doesn't fall back to input state being emptied
// when submit is clicked again.